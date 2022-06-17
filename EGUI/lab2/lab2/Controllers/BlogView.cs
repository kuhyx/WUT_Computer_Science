using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace lab2.Controllers
{
    public class BlogViewController : Controller
    {
        // 
        // GET: /Register/

        public IActionResult Index()
        {
            return View();
        }

        // 
        // GET: /Register/RegisterUser/?userid=Rick&email=4&password=test&blogid=blogtest

        public IActionResult RegisterUser(string userid, string email, string password, string blogid)
        {
            ViewData["userid"] = "userid: " + userid;
            ViewData["email"] = "email: " + email;
            ViewData["password"] = "password: " + password;
            ViewData["blogid"] = "blogid: " + blogid;
            return View();
        }
    }
}