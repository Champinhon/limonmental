# Importaciones de Django para vistas y autenticación
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

# Importaciones de tus aplicaciones y modelos
from .forms import CustomUserCreationForm, PostForm, CommentForm, PsychologistForm
from .models import Post, Comment, Psychologist

# Importaciones de terceros y estándar de Python
import json
import time
from openai import OpenAI

# Configura tu clave de API de OpenAI
LIMONCITO_ID =  ''

client = OpenAI(api_key = "")

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
'''
def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = f"http://{domain}/verify-email/{uid}/{token}/"

    subject = 'Verifica tu cuenta'
    message = f'Por favor, verifica tu cuenta haciendo clic en el siguiente enlace: {link}'
    send_mail(subject, message, 'contacto@limonmental.com', [user.email])'''
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
# Define una función para enviar un mensaje al asistente
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(LIMONCITO_ID, thread, user_input)
    return thread, run
'''
def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.profile.email_verified = True  # Asumiendo que tienes un campo 'email_verified' en tu modelo de perfil
        user.profile.save()
        # Redirigir a una página de éxito o similar
        return redirect('success_page')
    else:
        # Redirigir a una página de error o similar
        return redirect('error_page')'''
# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.2)
    return run

def limoncito(mensaje):
    thread1, run1 = create_thread_and_run(
    mensaje
    )
    run1 = wait_on_run(run1, thread1)
    messages = get_response(thread1)
    
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value
@login_required
def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            message = body.get('message', '')
            response = limoncito(message)
            print(response)
            return JsonResponse({'message': message, 'response': response})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        return render(request, 'chat/chatbot.html')

    return JsonResponse({'error': 'Método no permitido'}, status=405)
def psychologists(request):
    psychologists_list = Psychologist.objects.all()
    query = request.GET.get('q')
    tipo_consulta = request.GET.get('tipo_consulta')    
    especialidad = request.GET.get('especialidad')

    if query:
        psychologists_list = [psychologist for psychologist in psychologists_list if query.lower() in psychologist.name.lower()]

    if tipo_consulta:
        psychologists_list = [psychologist for psychologist in psychologists_list if tipo_consulta.lower() == psychologist.tipo_consulta.lower()]

    if especialidad:
        psychologists_list = [psychologist for psychologist in psychologists_list if especialidad.lower() in psychologist.especialidad.lower()]

    for psychologist in psychologists_list:
        psychologist.photo_url = psychologist.get_photo_url()

    return render(request, 'psychologists.html', {'psychologists_list': psychologists_list, 'query': query, 'tipo_consulta': tipo_consulta, 'especialidad': especialidad })

def is_admin(user):
    return user.is_staff

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_staff or request.user == comment.author:
        comment.delete()
    return redirect('posts')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_staff or request.user == post.author:
        post.delete()
        return redirect('posts') 

    return HttpResponse("No tienes permisos para borrar este post.")

def post_list(request):
    posts = Post.objects.order_by('-created_at') 
    context = {'latest_posts': posts}
    if is_admin(request.user):
        return render(request, 'posts/post_list.html', context)
    else:
        return render(request, 'posts/post_list.html', context)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_list')
    else:
        form = CommentForm()

    return render(request, 'posts/create_comment.html', {'form': form, 'post': post})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Mensaje de error si la autenticación falla
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')

    return render(request, 'registration/login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
def post_search(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    context = {'latest_posts': posts, 'query': query}
    return render(request, 'posts/post_list.html', context)

def home(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
    else:
        posts = posts.order_by('-created_at')[:3]

    context = {'latest_posts': posts, 'query': query}
    return render(request, 'home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
        else:
            form = CommentForm()
    else:
        form = None

    context = {
        'post': post,
        'comment_form': form,
    }

    return render(request, 'posts/post_detail.html', context)

@login_required
def paypal(request):
    return render(request, 'paypal.html')


def error_404(request, exception):
    return render(request, '404.html', status=404)

def blog(request):
    return render(request, 'blog.html')
@login_required
@user_passes_test(is_admin)
def create_psychologist(request):
    if request.method == 'POST':
        form = PsychologistForm(request.POST, request.FILES)
        if form.is_valid():
            psychologist = form.save()
            return redirect('psychologist_detail', pk=psychologist.pk)
    else:
        form = PsychologistForm()
    return render(request, 'create_psicologo.html', {'form': form})
def psychologist_detail(request, pk):
    psychologist = get_object_or_404(Psychologist, pk=pk)
    # Tu lógica para mostrar los detalles del psicólogo
    return render(request, 'psychologist_detail.html', {'psychologist': psychologist})



def delete_psychologist(request, pk):
    psychologist = get_object_or_404(Psychologist, pk=pk)

    if request.method == 'POST':
        psychologist.delete()
        messages.success(request, 'Psicólogo eliminado correctamente.')
        return redirect('home')
    else:
        return render(request, 'delete_psychologist_confirmation.html', {'psychologist': psychologist})
