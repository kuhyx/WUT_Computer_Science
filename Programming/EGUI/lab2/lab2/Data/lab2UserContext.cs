#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using lab2.Models;

    public class lab2UserContext : DbContext
    {
        public lab2UserContext (DbContextOptions<lab2UserContext> options)
            : base(options)
        {
        }

        public DbSet<lab2.Models.User> User { get; set; }
    }
