import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import BlogEntry from "./components/pages/blogEntry/BlogEntry";
import { Context } from "./context/Context";
import CreateEntry from "./components/pages/createEntry/CreateEntry";
import Home from "./components/pages/home/Home";
import Login from "./components/pages/Login/Login";
import Register from "./components/pages/Register/Register";
import TopBar from "./components/topbar/TopBar";
import { useContext } from "react";

function App() {
  const {user} = useContext(Context);
  console.log("logged: " + user);
  return (
    <BrowserRouter>
    <TopBar/>
    <Routes>
      <Route path="/" element={<Home />} />
        <Route exact path="login"  element={user ? <Home/> :<Login />}/>
        <Route exact path="/register" element={user ? <Home/> : <Register />} />
        <Route exact path="createEntry" element={user ? <CreateEntry /> : <Home/> } />
        <Route path="blogEntry/:entryId" element={<BlogEntry />} />

    </Routes>
  </BrowserRouter>
  );
}

export default App;
