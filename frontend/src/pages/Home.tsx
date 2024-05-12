import { useAuthState, useSignInWithGoogle } from 'react-firebase-hooks/auth';
import { Triangle } from 'react-loader-spinner';
import Welcome from '../components/Welcome';
import { auth } from '../firebase';
import googleLogo from '../assets/google.svg';

function Home() {
  const [user, userLoading] = useAuthState(auth);
  const [signInWithGoogle] = useSignInWithGoogle(auth);

  return (
    <main className="flex flex-col items-center mt-16 mx-4 text-center">
      <h2 className="text-2xl font-medium mb-8">
        Find the perfect movie to watch tonight.
      </h2>
      {userLoading && <Triangle />}
      {!userLoading && !user && (
        <>
          <p className="mt-4">But first you need to log in:</p>
          <button
            type="button"
            onClick={() => signInWithGoogle()}
            className="mt-10 flex items-center gap-2 border rounded-full py-2 px-4 border-gray-400 hover:bg-gray-700 duration-100"
          >
            <img src={googleLogo} alt="Google" className="size-8" />
            <span>Log in with Google</span>
          </button>
        </>
      )}
      {!!user && <Welcome />}
    </main>
  );
}

export default Home;
