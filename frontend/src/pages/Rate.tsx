import axios from 'axios';
import { useState } from 'react';
import { ThreeDots } from 'react-loader-spinner';
import useSWR, { Fetcher } from 'swr';
import RateMovie from '../components/RateMovie';
import TMDBMovie from '../types/TMDBMovie';

const fetcher: Fetcher<TMDBMovie[], string> = async (url) => {
  const res = await axios.get(url, {
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_TMDB_BEARER_TOKEN}`,
    },
  });

  return res.data.results as TMDBMovie[];
};

function Rate() {
  const [value, setValue] = useState('');

  const tmdbQuery = value
    ? `https://api.themoviedb.org/3/search/movie?query=${value}`
    : `https://api.themoviedb.org/3/trending/movie/day`;

  const { data, isLoading } = useSWR(tmdbQuery, fetcher);

  return (
    <main className="flex flex-col items-center px-6">
      <h2 className="text-2xl font-medium">Rate a movie</h2>
      <div className="max-w-full w-[600px]">
        <input
          type="text"
          placeholder="Find a movie..."
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="mt-12 bg-gray-700 rounded-full py-2 px-4 mb-12 w-full"
        />
      </div>
      {isLoading && <ThreeDots />}
      {!isLoading && !data?.length && <p>Could not find a movie 😬</p>}
      {!isLoading && !!data?.length && (
        <section className="flex flex-wrap gap-x-6 gap-y-9 justify-center">
          {data.slice(0, 12).map((movie) => (
            <RateMovie movie={movie} key={movie.id} />
          ))}
        </section>
      )}
    </main>
  );
}

export default Rate;
