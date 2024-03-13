from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager): 
    # 해당 함수가 모듈 또는 클래스의 외부에서 직접 호출되지 않고,해당 모듈 또는 클래스 내부에서만 사용되게 설정
    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 입력 항목입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        if extra_fields.get("is_superuser") is True:
            raise ValueError("일반유저를 슈퍼유저로 생성할 수 없습니다")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        superuser = self._create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    # email 이 username 역할하게 하기위해 AbstractBaseUser 상속받음
    # AbstractBaseUser 모델을 상속받아 권한관련 기능 추가를 위해 PermissionsMixin 상속받음
    email = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255)
    # 전부 슈퍼유저로 만들어지는것을 방지하기 위함
    # 권한과 관련된 부분
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    # 원래는 username 을 필요로 하는데 우리는 이걸 email 로 설정하기위해 바꿔줌 (username 사용 X)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return f"email: {self.email}, nickname: {self.nickname}"
