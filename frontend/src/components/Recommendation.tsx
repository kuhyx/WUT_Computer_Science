import axios from 'axios';
import { useEffect, useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import IRecommendation from '../types/Recommendation';
import TMDBMovie from '../types/TMDBMovie';
import posterPlaceholder from '../assets/poster_placeholder.svg';

interface RecommendationProps {
  recommendation: IRecommendation;
}

function Recommendation({ recommendation }: RecommendationProps) {
  const [movie, setMovie] = useState<TMDBMovie | null>(null);

  useEffect(() => {
    (async () => {
      const url = `https://api.themoviedb.org/3/movie/${recommendation.movieId}`;

      const res = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${import.meta.env.VITE_TMDB_BEARER_TOKEN}`,
        },
      });

      const movieDetails = res.data as TMDBMovie;

      setMovie(movieDetails);
    })();
  }, [recommendation.movieId]);

  if (!movie) return null;

  const posterUrl = `https://image.tmdb.org/t/p/w154${movie.poster_path}`;

  return (
    <article className="flex flex-col items-center w-[250px]">
      <img
        src={movie.poster_path ? posterUrl : posterPlaceholder}
        alt={movie.title}
        className="w-[154px] h-[231px] object-contain mb-2"
      />
      <h3 className="my-auto text-lg text-center text-gray-200 font-medium">
        {movie.title}
      </h3>
      <CircularProgressbar
        value={recommendation.match}
        text={`${recommendation.match}%`}
        className="size-[75px] mt-4"
        strokeWidth={11}
        circleRatio={0.75}
        styles={buildStyles({
          rotation: 1 / 2 + 1 / 8,
          strokeLinecap: 'butt',
          trailColor: '#eee',
          textSize: '24px',
          textColor: '#fff',
        })}
      />
    </article>
  );
}

export default Recommendation;
