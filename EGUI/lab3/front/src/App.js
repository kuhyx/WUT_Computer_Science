import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import BlogEntry from "./components/pages/blogEntry/BlogEntry";
import CreateEntry from "./components/pages/createEntry/CreateEntry";
import Home from "./components/pages/home/Home";
import Login from "./components/pages/Login/Login";
import Register from "./components/pages/Register/Register";
import TopBar from "./components/topbar/TopBar";

function App() {
  const logged = false;
  return (
    <BrowserRouter>
    <TopBar/>
    <Routes>
      <Route path="/" element={<Home />} />
        <Route exact path="login" element={logged ? <Home/> :<Login />}/>
        <Route exact path="/register" element={logged ? <Home/> : <Register />} />
        <Route exact path="createEntry" element={logged ? <CreateEntry /> : <Home/> } />
        <Route path="blogEntry/:entryId" element={<BlogEntry />} />

    </Routes>
  </BrowserRouter>
  );
}

export default App;
