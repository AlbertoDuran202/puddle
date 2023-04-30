import instaloader
from django.conf import settings

def get_instagram_images(username, max_images=6):
    L = instaloader.Instaloader()
    
    # Autenticarse con tus propias credenciales de Instagram
    L.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)

    profile = instaloader.Profile.from_username(L.context, username)

    if profile.is_private:
        return []  # Si el perfil es privado, regresa una lista vacía.

    images = []
    count = 0
    for post in profile.get_posts():
        images.append(post.url)
        count += 1
        if count >= max_images:
            break

    return images

