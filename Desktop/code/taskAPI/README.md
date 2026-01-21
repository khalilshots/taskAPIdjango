Task API – Django REST Framework (Learning Project)

This project is a basic but fully functional backend API built with Django REST Framework (DRF).
Its purpose is learning, not production: to understand how authentication, permissions, models, serializers, and viewsets work together to form a real backend.

1. What this backend is

This backend provides:

JWT-based authentication (Bearer tokens)

Authenticated CRUD operations on tasks

User ownership and access control

Clean separation of concerns (models, serializers, views)

It follows real API patterns, not Django-admin-only patterns.

2. Authentication (JWT – the “real API way”)
Why JWT?

APIs are usually consumed by:

mobile apps

frontend SPAs (React, Vue)

other backends

They do not rely on browser sessions.
Instead, every request proves identity using a Bearer token.

How JWT is configured

We use SimpleJWT:

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}


What this means:

Every request must include a valid JWT

If authentication succeeds, request.user is set

If it fails, the request is rejected before the view runs

Authentication endpoints
path("api/auth/token/", TokenObtainPairView.as_view()),
path("api/auth/token/refresh/", TokenRefreshView.as_view()),


POST /api/auth/token/ → login with username/password, receive tokens

POST /api/auth/token/refresh/ → refresh access token

The access token is sent with every request:

Authorization: Bearer <access_token>

3. Permissions vs Authentication

These are different concepts:

Authentication

Who are you?

Handled by:

JWTAuthentication

Sets request.user

Permissions

Are you allowed to do this?

Handled by:

IsAuthenticated

Custom permission classes if needed

Because IsAuthenticated is set globally, we do not need to repeat it in every view unless we want different behavior.

4. Models (Data layer)
Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


Key ideas:

Tasks belong to a user (owner)

Ownership is enforced at the query level

We reuse Django’s built-in User model

5. Serializers (API boundary)

Serializers are used when:

validating incoming request data

converting models to JSON responses

They are not used for authentication itself.

TaskSerializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["owner"]


What it does:

Validates incoming task data

Controls what fields are exposed

Converts model instances into JSON

UserSerializer (when needed)

User serializers are not required for login.

They are only needed when:

returning user data from the API

building endpoints like /api/me/

embedding user info in other responses

Example:

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

6. Views and ViewSets (Request handling)
Why ViewSets?

ViewSets:

reduce boilerplate

automatically implement CRUD

are common in real DRF projects

TaskViewSet
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


What happens here:

get_queryset()
Ensures users only see their own tasks

perform_create()
Automatically assigns task ownership on creation

This enforces authorization at the data level, not just the UI.

7. Routers (Automatic endpoints)
router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")


This automatically creates:

Method	Endpoint	Action
GET	/api/tasks/	list
POST	/api/tasks/	create
GET	/api/tasks/{id}/	retrieve
PUT	/api/tasks/{id}/	update
PATCH	/api/tasks/{id}/	partial update
DELETE	/api/tasks/{id}/	delete

No manual URL definitions are required.

8. Why no UserViewSet by default?

A full /api/users/ endpoint:

allows user enumeration

creates privacy risks

is rarely needed

Instead, APIs usually expose:

/api/me/ → current user profile

or user data embedded in other endpoints

User serializers and views are added only when there is a real use case (friends, profiles, social features).

9. Business logic placement

Rule of thumb:

Views: HTTP orchestration

Serializers: validation & formatting

Models: data + model-specific behavior

Services: reusable business logic

Example:

def multiply_by_seven(value: int) -> int:
    return value * 7


Views call services — views do not contain business rules.

10. Health check example (no serializer needed)
class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


Health checks:

do not expose models

do not validate complex input

do not require serializers

11. What this project demonstrates

This project shows:

JWT-based authentication

Proper permission handling

Ownership-based authorization

Clean DRF architecture

Separation of concerns

A backend that works independently of the frontend

It is intentionally simple, but structurally correct.

12. Who this project is for

Someone learning backend APIs

Someone transitioning from Django admin to real APIs

Someone wanting a clean DRF reference project




.gitignore mental model


Environment

.venv/

.env

Generated by Python

__pycache__/

*.pyc

Generated by framework

db.sqlite3

migrations/* (sometimes)

Generated by OS

.DS_Store



