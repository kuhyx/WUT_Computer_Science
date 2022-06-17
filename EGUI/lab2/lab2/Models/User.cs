using System.ComponentModel.DataAnnotations;

namespace lab2.Models
{
    public class User
    {
        public string? Id { get; set; }
        public string? email { get; set; }
        public string? password { get; set; }
    }
}