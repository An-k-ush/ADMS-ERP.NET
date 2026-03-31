using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using ADMS.ERP.Models;

namespace ADMS.ERP.Data
{
    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Item> Items { get; set; }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            builder.Entity<Item>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
                entity.Property(e => e.Weight).HasColumnType("decimal(18,4)");
                entity.Property(e => e.Description).HasMaxLength(500);

                // Self-referencing relationship
                entity.HasOne(e => e.ParentItem)
                      .WithMany(e => e.ChildItems)
                      .HasForeignKey(e => e.ParentItemId)
                      .OnDelete(DeleteBehavior.Restrict)
                      .IsRequired(false);

                entity.HasIndex(e => e.Name);
                entity.HasIndex(e => e.ParentItemId);
            });
        }
    }
}
