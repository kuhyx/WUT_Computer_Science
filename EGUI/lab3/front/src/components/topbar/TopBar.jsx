import 'bootstrap/dist/css/bootstrap.min.css';

import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar'

export default function TopBar() {
  const logged = false;
    return (
<Navbar bg="light" expand="lg">
  <Container>
    <Navbar.Brand href="">Lab 3 Blog</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="/">Home</Nav.Link>
        <Nav.Link href="/login">{logged ? "" : "Login"}</Nav.Link>
        <Nav.Link href="/register">{logged ? "" : "Register"}</Nav.Link>
        <Nav.Link href="/createEntry"> {logged ? "Create entry" : ""}</Nav.Link>
        </Nav>
    </Navbar.Collapse>
  </Container>
</Navbar>
    )
}
