// AppRoutes.js
import { createBrowserRouter } from 'react-router-dom';
import App from '../App';
import Home from '../components/pages/home';
// import CourseList from '../components/CourseList'; 
// import CourseDetail from '../components/CourseDetail'; 
// import TopicList from '../components/TopicList';
// import TopicDetail from '../components/TopicDetail';
// import NoteList from '../components/NoteList'; 
// import NoteDetail from '../components/NoteDetail'; 
// import QuizDetail from '../components/QuizDetail'; 
// import ProfileDetail from '../components/ProfileDetail';
// import ProfileDetailForm from '../components/ProfileDetailForm'; 
// import CourseForm from '../components/CourseForm'; 
// import TopicForm from '../components/TopicForm'; 
// import NoteForm from '../components/NoteForm'; 
import Registration from '../components/auth/Registration';
// import NotFound from '../components/NotFound'; 
// import ErrorPage from '../components/ErrorPage'; 

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        index: true,
        element: <Home />
      },
      // {
      //   path: "courses",
      //   element: <CourseList />
      // },
      // {
      //   path: "courses/new",
      //   element: <CourseForm />
      // },
      // {
      //   path: "courses/:courseId",
      //   element: <CourseDetail />,
      //   children: [
      //     {
      //       path: "edit",
      //       element: <CourseForm />
      //     },
      //     {
      //       path: "topics",
      //       element: <TopicList />
      //     },
      //     {
      //       path: "topics/new",
      //       element: <TopicForm />
      //     },
      //     {
      //       path: "topics/:topicId",
      //       element: <TopicDetail />,
      //       children: [
      //         {
      //           path: "edit",
      //           element: <TopicForm />
      //         },
      //         {
      //           path: "notes",
      //           element: <NoteList />
      //         },
      //         {
      //           path: "notes/new",
      //           element: <NoteForm />
      //         },
      //         {
      //           path: "notes/:noteId",
      //           element: <NoteDetail />,
      //           children: [
      //             {
      //               path: "edit",
      //               element: <NoteForm />
      //             }
              //   ]
              // }
            // ]
          // }
        // ]
      // },
    //   {
    //     path: "courses/:courseId/topics/:topicId/quizzes",
    //     element: <QuizList />
    //   },
    //   {
    //     path: "courses/:courseId/topics/:topicId/quizzes/:quizId",
    //     element: <QuizDetail />
    //   },
    //   {
    //     path: "profile",
    //     element: <ProfileDetail />
    //   },
      // {
      //   path: "profile/edit",
      //   element: <ProfileDetailForm />
      //   },
      //   {
      //   path: "notes/",
      //   element: <NoteList/>,
      // },
      // {
      //   path: "notes/:noteId",
      //   element: <NoteDetail />,
      // },
        {
            path: "registration",
            element: <Registration />
        },
      // {
      //   path: "*",
      //   element: <NotFound />
      // },
      // {
      //   path: "/error",
      //   element: <ErrorPage />
      // }
    ]
  }
]);

export default router;