using System.ComponentModel.DataAnnotations;

namespace ADMS.ERP.Models
{
    public class ProcessItemViewModel
    {
        [Required(ErrorMessage = "Please select a parent item.")]
        [Display(Name = "Parent Item")]
        public int ParentItemId { get; set; }

        public List<ChildItemInput> ChildItems { get; set; } = new List<ChildItemInput>();

        // For populating dropdown
        public List<Item>? AvailableItems { get; set; }
    }

    public class ChildItemInput
    {
        [Required(ErrorMessage = "Child item name is required.")]
        [StringLength(200, MinimumLength = 1, ErrorMessage = "Name must be between 1 and 200 characters.")]
        [Display(Name = "Item Name")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Weight is required.")]
        [Range(0.01, double.MaxValue, ErrorMessage = "Weight must be greater than 0.")]
        [Display(Name = "Weight (kg)")]
        public decimal Weight { get; set; }

        [StringLength(500)]
        public string? Description { get; set; }
    }

    public class ItemSearchViewModel
    {
        public string? SearchTerm { get; set; }
        public List<Item> Results { get; set; } = new List<Item>();
    }

    public class TreeNodeViewModel
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public decimal Weight { get; set; }
        public bool IsProcessed { get; set; }
        public List<TreeNodeViewModel> Children { get; set; } = new List<TreeNodeViewModel>();
        public int? ParentItemId { get; set; }
    }
}
