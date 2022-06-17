using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace lab2.Controllers
{
    public class LoginController : Controller
    {
        // 
        // GET: /Login/

        public IActionResult Index()
        {
            return View();
        }

        // 
        // GET: /Login/LoginUser/
        // https://localhost:{PORT}/Login/LoginUser/?userid=Rick&password=4

        public IActionResult LoginUser(string userid, string password)
        {
            ViewData["userid"] = "userid: " + userid;
            ViewData["password"] = "password: " + password;

            return View();
        }
    }
}