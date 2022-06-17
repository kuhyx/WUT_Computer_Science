using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Web;
using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace FormEncode.Controllers
{
    public class RegisterController : Controller
    {


        [HttpPost]
        [ActionName("Complex")]
        public IActionResult PostComplex(string id, string blogid, string blogTitle, string mail, string password)
        {
            if(id != null && blogid != null && blogTitle != null && mail != null & password != null)
            {
                // Convert any HTML markup in the status text.
                id = HttpUtility.HtmlEncode(id);
                blogid = HttpUtility.HtmlEncode(blogid);
                blogTitle = HttpUtility.HtmlEncode(blogTitle);
                mail = HttpUtility.HtmlEncode(mail);
                password = HttpUtility.HtmlEncode(password);
                ViewData["userid"] = "userid: " + id;
                ViewData["email"] = "email: " + mail;
                ViewData["password"] = "password: " + password;
                ViewData["blogid"] = "blogid: " + blogid;
                ViewData["blogtitle"] = "blogtitle: " + blogTitle;
                return View();
            }
            else return View();
        }
        // 
        // GET: /Register/

        public IActionResult Index()
        {
            return View();
        }

        // 
        // GET: /Register/RegisterUser/?userid=Rick&email=4&password=test&blogid=blogtest

        public IActionResult RegisterUser(string userid, string email, string password, string blogid, string blogtitle)
        {
            ViewData["userid"] = "userid: " + userid;
            ViewData["email"] = "email: " + email;
            ViewData["password"] = "password: " + password;
            ViewData["blogid"] = "blogid: " + blogid;
            ViewData["blogtitle"] = "blogtitle: " + blogtitle;
            return View();
        }
    }
}