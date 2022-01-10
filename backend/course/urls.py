from django.conf.urls import url
from django.urls import path, include
from rest_framework import views
from .views import CourseListView, deleteCourseView, getCourseView, updateCourseView, addCourseView, getAllCourse,getFrontCourseInfoView
from .views import SectionListView, deleteSectionView, getSectionView, updateSectionView, addSectionView,getAllSectionSec_id,TakeSectionListView,TeachSectionListView,getFrontSectionInfoView
from .views import Time_slotListView, getAllTime_slotView, updateTime_slotView, getAllTime_slotSelectView
from .views import ClassroomListView, deleteClassroomView, getClassroomView, updateClassroomView, addClassroomView,getAllClassroom
from .views import TakeListView, deleteTakeView, getTakeView, updateTakeView, addTakeView
from .views import TeachListView, deleteTeachView, getTeachView, updateTeachView, addTeachView

urlpatterns = [
    path('pageCourseCondition/', CourseListView.as_view()),
    url(r'^deleteCourse/(?P<pk>[0-9]+)$', deleteCourseView.as_view()),
    url(r'^getCourse/(?P<pk>[0-9]+)$', getCourseView.as_view()),
    url(r'^updateCourse/(?P<pk>[0-9]+)$',updateCourseView.as_view()),
    path('addCourse/', addCourseView.as_view()),
    path('getAllCourse/', getAllCourse.as_view()),

    path('getFrontCourse/', CourseListView.as_view()),
    url(r'^getFrontCourseInfo/(?P<pk>[0-9]+)$', getFrontCourseInfoView.as_view()),



    path('pageSectionCondition/', SectionListView.as_view()),
    url(r'^deleteSection/(?P<pk>[0-9]+)$', deleteSectionView.as_view()),
    url(r'^getSection/(?P<pk>[0-9]+)$', getSectionView.as_view()),
    url(r'^updateSection/(?P<pk>[0-9]+)$',updateSectionView.as_view()),
    path('addSection/', addSectionView.as_view()),
    path('getAllSectionSec_id/', getAllSectionSec_id.as_view()),
    # 特别的部分
    path('pageTakeSectionCondition/', TakeSectionListView.as_view()),
    path('pageTeachSectionCondition/', TeachSectionListView.as_view()),

    url(r'^getFrontSectionInfo/(?P<pk>[0-9]+)$', getFrontSectionInfoView.as_view()),



    path('Time_slotCondition/', Time_slotListView.as_view()),
    url(r'^getAllTime_slot/', getAllTime_slotView.as_view()),
    url(r'^getAllTime_slotSelect/', getAllTime_slotSelectView.as_view()),
    url(r'^updateTime_slot/',updateTime_slotView.as_view()),


    path('pageClassroomCondition/', ClassroomListView.as_view()),
    url(r'^deleteClassroom/(?P<pk>[0-9]+)$', deleteClassroomView.as_view()),
    url(r'^getClassroom/(?P<pk>[0-9]+)$', getClassroomView.as_view()),
    url(r'^updateClassroom/(?P<pk>[0-9]+)$',updateClassroomView.as_view()),
    path('addClassroom/', addClassroomView.as_view()),
    path('getAllClassroom/', getAllClassroom.as_view()),



    path('pageTeachCondition/', TeachListView.as_view()),
    url(r'^deleteTeach/(?P<pk>[0-9]+)$', deleteTeachView.as_view()),
    url(r'^getTeach/(?P<pk>[0-9]+)$', getTeachView.as_view()),
    url(r'^updateTeach/(?P<pk>[0-9]+)$',updateTeachView.as_view()),
    path('addTeach/', addTeachView.as_view()),
    # path('getAllTeach/', getAllTeach.as_view()),



    path('pageTakeCondition/', TakeListView.as_view()),
    url(r'^deleteTake/(?P<pk>[0-9]+)$', deleteTakeView.as_view()),
    url(r'^getTake/(?P<pk>[0-9]+)$', getTakeView.as_view()),
    url(r'^updateTake/(?P<pk>[0-9]+)$',updateTakeView.as_view()),
    path('addTake/', addTakeView.as_view()),
    # path('getAllTake/', getAllTake.as_view()),

]
