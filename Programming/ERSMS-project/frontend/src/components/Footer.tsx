import tmdb from '../assets/tmdb.svg';

function Footer() {
  return (
    <div className="mt-auto mx-auto">
      <footer className="py-6 px-4 mt-16 flex flex-col items-center gap-4">
        <a
          href="https://www.themoviedb.org"
          target="_blank"
          className="underline"
        >
          <img src={tmdb} alt="The Movie Database" className="w-[180px]" />
        </a>
        <small className="text-sm text-[#a0d7d8] text-center leading-relaxed">
          <span>This product uses the </span>
          <a
            href="https://www.themoviedb.org"
            target="_blank"
            className="underline"
          >
            TMDB
          </a>
          <span> API but is not endorsed or certified by TMDB.</span>
        </small>
      </footer>
    </div>
  );
}

export default Footer;
