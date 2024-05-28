import { useAuthState } from 'react-firebase-hooks/auth';
import { ThreeDots } from 'react-loader-spinner';
import useSWR, { Fetcher } from 'swr';
import Recommendation from '../components/Recommendation';
import Refresh from '../components/Refresh';
import { auth } from '../firebase';
import IRecommendation from '../types/Recommendation';

const fetcher: Fetcher<IRecommendation[], string> = async (userId) => {
  const res = {
    data: {
      userId,
      recommendations: [
        { movieId: 174, match: 78 },
        { movieId: 70, match: 74 },
        { movieId: 421, match: 70 },
        { movieId: 5846, match: 54 },
        { movieId: 926, match: 48 },
      ],
    },
  };

  await new Promise((res) => setTimeout(res, 2500));

  return res.data.recommendations as IRecommendation[];
};

function Recommendations() {
  const [user] = useAuthState(auth);

  if (!user) throw new Error('User not found');

  const { data, isLoading, isValidating, mutate } = useSWR(user.uid, fetcher);

  return (
    <main className="flex flex-col items-center px-6 flex-1">
      <h2 className="text-2xl font-medium">Recommendations</h2>
      {isLoading && (
        <div className="my-auto flex flex-col items-center gap-2">
          <ThreeDots />
          <p className="italic">Loading recommendations...</p>
        </div>
      )}
      {!isLoading && <Refresh mutate={mutate} isValidating={isValidating} />}
      {!isLoading && !data?.length && (
        <p>Could not find any recommendations for you 😬</p>
      )}
      {!isLoading && !!data?.length && (
        <section className="flex flex-wrap gap-x-6 gap-y-9 justify-center">
          {data.map((recommendation) => (
            <Recommendation
              recommendation={recommendation}
              key={recommendation.movieId}
            />
          ))}
        </section>
      )}
    </main>
  );
}

export default Recommendations;
