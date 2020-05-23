from django.shortcuts import render, redirect
from .models import Candidate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import CandidateForm, AuthUserForm, RegisterUserForm, CommentForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, AnonymousUser
from voting.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text


logger = logging.getLogger('django')


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != 'admin':
            logger.info("User " + str(request.user.username) + ' is trying to use admin permissions')
            return self.handle_no_permission()
        else:
            logger.info("Admin use special permissions")

        return super().dispatch(request, *args, **kwargs)


class HomePage(ListView):

    model = Candidate
    template_name = "index.html"
    context_object_name = 'candidates'

    def get_context_data(self, **kwargs):
        kwargs['candidates'] = Candidate.objects.all().order_by('-votes')
        return super().get_context_data(**kwargs)


class CandidatePage(FormMixin, DetailView):
    model = Candidate
    template_name = 'candidate.html'
    context_object_name = 'candidate_id'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('candidate_page', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            logger.info("Successfully adding comment")
            return self.form_valid(form)
        else:
            logger.error("User can't adding comment")
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.candidate = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class CandidateCreateView(AdminRequiredMixin, CreateView):
    model = Candidate
    template_name = 'edit_candidates.html'
    form_class = CandidateForm
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['candidates_list'] = Candidate.objects.all().order_by('-votes')
        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name = 'login_form.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        logger.info('Successfully going to home page')
        return self.success_url


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class UserRegisterView(CreateView):
    model = User
    template_name = 'register_form.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = "Аккаунт успешно создан!"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        logger.info("User " + username + " is successfully register")

        return form_valid


class CandidateUpdateView(AdminRequiredMixin, UpdateView):
    model = Candidate
    template_name = 'edit_candidates.html'
    form_class = CandidateForm
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class CandidateDeleteView(AdminRequiredMixin, DeleteView):
    model = Candidate
    template_name = 'edit_candidates.html'
    success_url = reverse_lazy('edit_page')


@login_required
def vote_for_candidate(request):
    candidate_id = request.GET.get('candidate_id', None)
    if candidate_id is not None:
        success = not request.user.profile.is_voted
        if success:
            request.user.profile.vote()
            candidate = Candidate.objects.get(pk=candidate_id)
            candidate.inc_votes()
            logger.info('User ' + str(request.user.username) + ' is successfully voting')
        else:
            logger.info('User ' + str(request.user.username) + ' is trying to vote, when already voting')

    else:
        logger.error("Voting for NONE candidate")
        success = False

    data = {'success' : success}
    return JsonResponse(data)


def usersignup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Активация аккаунта'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Мы отправили вам письмо, пожалуйста, подтвердите ваш e-mail для завершения регистрации!')
    else:
        form = RegisterUserForm()

    return render(request, 'register_form.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')