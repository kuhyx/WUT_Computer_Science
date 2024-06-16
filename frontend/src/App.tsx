import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import Home from './pages/Home';
import Recommendations from './pages/Recommendations';
import Rate from './pages/Rate';
import Analytics from './pages/Analytics';

function App() {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Layout />,
      children: [
        { path: '/', element: <Home /> },
        { path: '/recommendations', element: <Recommendations /> },
        { path: '/rate', element: <Rate /> },
        { path: '/analytics', element: <Analytics /> },
        { path: '*', element: <code>404</code> },
      ],
    },
  ]);

  return <RouterProvider router={router} />;
}

export default App;
