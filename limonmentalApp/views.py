# Importaciones de Django para vistas y autenticación
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Importaciones de tus aplicaciones y modelos
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PostForm, CommentForm
from .models import Post, Comment

# Importaciones de terceros y estándar de Python
import json
import time
import openai 

def limoncito(mensaje):
    chat_history = []
    try:
        openai.api_key = "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"
        if mensaje == "exit":
            return "Adiós, gracias por usar Limoncito."
        elif mensaje == "como te llamas" or mensaje == "cómo te llamas" or mensaje == "como te llamas?" or mensaje == "cómo te llamas?" or mensaje ==  "Cómo te llamas" or mensaje ==  "Como te llamas" or mensaje ==  "Cómo te llamas?" or mensaje ==  "Como te llamas?" or mensaje ==  "¿Cómo te llamas?" or mensaje ==  "¿Como te llamas?" or mensaje ==  "¿Cómo te llamas" or mensaje ==  "¿Como te llamas" or mensaje ==  "¿Cómo te llamas?" or mensaje ==  "¿Como te llamas?" or mensaje ==  "¿cómo te llamas" or mensaje ==  "¿como te llamas" or mensaje ==  "¿cómo te llamas?" or mensaje ==  "¿como te llamas?":
            return "Mi nombre es Limoncito."
        else:
            chat_history.append({"role": "user", "content": f'{mensaje}'})
            response_iterator = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = chat_history,
                stream=True,
            )
            collected_messages = []
            for chunk in response_iterator:
                chunk_message = chunk['choices'][0]['delta'] 
                collected_messages.append(chunk_message) 
                full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
                print(full_reply_content)

                print("\033[H\033[J", end="")

            chat_history.append({"role": "assistant", "content": full_reply_content})
            full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
            print(f"GPT: {full_reply_content}")
            return full_reply_content
    except Exception as e:
        print(f"Error: {e}")
        return "Lo siento, hubo un error al procesar tu solicitud."
def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            message = body.get('message', '')
            response = limoncito(message)
            return JsonResponse({'message': message, 'response': response})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        return render(request, 'chat/chatbot.html')

    return JsonResponse({'error': 'Método no permitido'}, status=405)
def psychologists(request):
    psychologists_list = [
        {"name": "Psicólogo 1", "photo": "https://storage.googleapis.com/limonmental/Disen%CC%83o%20sin%20ti%CC%81tulo%20(5).png", "description": "Descripción del psicólogo 1", "tipo_consulta": "Virtual", "especialidad": "Especialidad 1", "precio": 10000},
        {"name": "Psicólogo 2", "photo": "https://storage.googleapis.com/limonmental/53875233-04FA-4805-B538-43655913EC1C.jpg", "description": "Descripción del psicólogo 2", "tipo_consulta": "Presencial", "especialidad": "Especialidad 2", "precio": 20000},
    ]

    query = request.GET.get('q')
    tipo_consulta = request.GET.get('tipo_consulta')
    especialidad = request.GET.get('especialidad')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')

    if query:
        psychologists_list = [psychologist for psychologist in psychologists_list if query.lower() in psychologist['name'].lower()]

    if tipo_consulta:
        psychologists_list = [psychologist for psychologist in psychologists_list if tipo_consulta.lower() == psychologist['tipo_consulta'].lower()]

    if especialidad:
        psychologists_list = [psychologist for psychologist in psychologists_list if especialidad.lower() in psychologist['especialidad'].lower()]

    if precio_min:
        psychologists_list = [psychologist for psychologist in psychologists_list if psychologist['precio'] >= int(precio_min)]

    if precio_max:
        psychologists_list = [psychologist for psychologist in psychologists_list if psychologist['precio'] <= int(precio_max)]

    return render(request, 'psychologists.html', {'psychologists_list': psychologists_list, 'query': query, 'tipo_consulta': tipo_consulta, 'especialidad': especialidad, 'precio_min': precio_min, 'precio_max': precio_max})

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
            # Aquí, si el formulario no es válido, se agregarán mensajes de error
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
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