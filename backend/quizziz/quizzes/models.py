from django.utils.translation import gettext as _
from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError


class DisplayNameAbstract(models.Model):
    display_name = models.CharField(max_length=50, unique=True)
    name = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.display_name)

        return super(DisplayNameAbstract, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Section(DisplayNameAbstract):
    pass


class Category(DisplayNameAbstract):
    pass


"""
TODO:
Make a model for each type of quiz
"""


class Quiz(models.Model):
    # CATEGORY = (
    #     ('general_knowledge', 'General knowledge'),
    #     ('celebrities', 'Celebrities'),
    #     ('for_kids', 'For kids'),
    #     ('movies', 'Movies'),
    #     ('geography', 'Geography'),
    #     ('history', 'History'),
    #     ('literature', 'Literature'),
    #     ('people', 'People'),
    #     ('music', 'Music'),
    #     ('science', 'Science'),
    #     ('policy', 'Policy'),
    #     ('nature', 'Nature'),
    #     ('psychology', 'Psychology'),
    #     ('religion', 'Religion'),
    #     ('entertainment', 'Entertainment'),
    #     ('sport', 'Sport'),
    #     ('technology', 'Technology'),
    #     ('television', 'Television'),
    #     ('funny', 'Funny'),
    #     ('puzzles', 'Puzzles'),
    #     ('health_and_beauty', 'Health and beauty'),
    #     ('animals', 'Animals'),
    # )

    # SECTION = (
    #     ('knowledge_quiz', 'Knowledge Quiz'),
    #     ('psychology_quiz', 'Psychology Quiz'),
    #     ('preferential_quiz', 'Preferential Quiz'),
    #     ('universal_quiz', 'Universal Quiz'),
    # )

    DEFAULT_IMAGE = 'https://cdn.pixabay.com/photo/2017/01/24/00/21/question-2004314_960_720.jpg'

    DEFAULT_DESCRIPTION = _('Welcome to my quiz!')

    author = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, related_name='quizzes')
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    section = models.ForeignKey(
        Section, on_delete=models.DO_NOTHING, default=1, related_name='quizzes')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, default=1, related_name='quizzes')
    image_url = models.URLField(default=DEFAULT_IMAGE)
    solved_times = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    random_question_order = models.BooleanField(default=True)
    password = models.CharField(max_length=20, blank=True)
    ask_name = models.BooleanField(default=True)
    ask_email = models.BooleanField(default=False)
    ask_gender = models.BooleanField(default=False)
    ask_opinion = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['author'], max_length=120)

    def __str__(self):
        return self.title


class QuizReview(models.Model):
    GENDER = (
        ('man', 'Man'),
        ('woman', 'Woman'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=80, blank=True)
    gender = models.CharField(max_length=5, choices=GENDER, blank=True)
    opinion = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    summery = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='question',
                         unique_with=['quiz'], max_length=120)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.answer

    class Meta:
        abstract = True


class KnowledgeAnswer(Answer):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='knowledge_answers')
    is_correct = models.BooleanField(default=False)


class PsychologyResults(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='psychology_results')
    result = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class PsychologyAnswer(Answer):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='psychology_answers')
    results = models.ManyToManyField(PsychologyResults)


class PreferentialAnswer(Answer):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='preferential_answers')
    answered_times = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.image_url and not(valid_url_extension(self.image_url)):
            raise EnvironmentError(
                f"Field 'image_url' got wrong URL, it should end with {[i for i in VALID_IMAGE_EXTENSIONS]}")

        return super(self.__class__, self).save(*args, **kwargs)


class UniversalAnswer(Answer):
    POINTS = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8),
        ('9', 9),
        ('10', 10),
    )

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='universal_answers')
    points = models.CharField(
        max_length=2, choices=POINTS, default=POINTS[0][0])
