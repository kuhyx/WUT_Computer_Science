import { useAuthState, useSignOut } from 'react-firebase-hooks/auth';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { auth } from '../firebase';

function Navbar() {
  const [user, userLoading] = useAuthState(auth);
  const [signOut] = useSignOut(auth);
  const navigate = useNavigate();

  const handleSignOut = () => {
    navigate('/');
    signOut();
  };

  return (
    <header className="px-6 py-4 flex justify-between items-center">
      <Link to="/">
        <h1 className="text-xl sm:text-2xl">Movie Recommendation</h1>
      </Link>
      {userLoading && <p>Loading user info</p>}
      {!userLoading && !user && (
        <p className="text-gray-300 text-lg">Logged out</p>
      )}
      {!!user && (
        <div className="flex gap-8">
          <nav>
            <ul className="flex flex-col text-center gap-4 md:flex-row">
              <li>
                <NavLink
                  to="/recommendations"
                  className={({ isActive }) => (isActive ? 'font-medium' : '')}
                >
                  Recommendations
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/rate"
                  className={({ isActive }) => (isActive ? 'font-medium' : '')}
                >
                  Rate
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/analytics"
                  className={({ isActive }) => (isActive ? 'font-medium' : '')}
                >
                  Analytics
                </NavLink>
              </li>
            </ul>
          </nav>
          <button onClick={handleSignOut}>Log out</button>
        </div>
      )}
    </header>
  );
}

export default Navbar;
