using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ADMS.ERP.Models
{
    public class Item
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Item name is required.")]
        [StringLength(200, MinimumLength = 1, ErrorMessage = "Item name must be between 1 and 200 characters.")]
        [Display(Name = "Item Name")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Weight is required.")]
        [Range(0.01, double.MaxValue, ErrorMessage = "Weight must be greater than 0.")]
        [Display(Name = "Weight (kg)")]
        public decimal Weight { get; set; }

        [StringLength(500)]
        public string? Description { get; set; }

        public bool IsProcessed { get; set; } = false;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime? UpdatedAt { get; set; }

        // Navigation: parent-child relationship
        public int? ParentItemId { get; set; }

        [ForeignKey(nameof(ParentItemId))]
        public Item? ParentItem { get; set; }

        public ICollection<Item> ChildItems { get; set; } = new List<Item>();
    }
}
