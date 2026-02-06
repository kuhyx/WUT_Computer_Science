import { useEffect } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { Triangle } from 'react-loader-spinner';
import { Outlet, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { auth } from './firebase';

function Layout() {
  const [user, userLoading] = useAuthState(auth);
  const navigate = useNavigate();

  useEffect(() => {
    if (!userLoading && !user) {
      navigate('/');
    }
  }, [navigate, user, userLoading]);

  return (
    <>
      <Navbar />
      {userLoading ? (
        <Triangle wrapperClass="m-auto" height={120} width={120} />
      ) : (
        <Outlet />
      )}
      <Footer />
    </>
  );
}

export default Layout;
