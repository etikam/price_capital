from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    #en creant un utilisateur, il faudrait que je n'oublie pas de passer son rol en parametrre de create_user
    def create_user(self, email, password=None, role='PHYSICAL', **extra_fields):

        if not email:
            raise ValueError('L\'adresse email doit être renseignée.')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.is_active = False #je le desactive jusqu'à ce qu'il valide son mail
        user.save(using=self._db)
        
    #creating profile with different roles 
        from .models import PhysicalPerson, MoralPerson
        if role == 'PHYSICAL':
            PhysicalPerson.objects.create(user=user)
        elif role == 'MORAL':
            MoralPerson.objects.create(user=user)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, role='ADMIN', **extra_fields)
