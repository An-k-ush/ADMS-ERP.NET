using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ADMS.ERP.Data;
using ADMS.ERP.Models;

namespace ADMS.ERP.Controllers
{
    [Authorize]
    public class ProcessController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ProcessController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: Process/Index - List of processed items
        public async Task<IActionResult> Index()
        {
            var processedItems = await _context.Items
                .Include(i => i.ChildItems)
                .Where(i => i.IsProcessed)
                .OrderByDescending(i => i.UpdatedAt ?? i.CreatedAt)
                .ToListAsync();

            return View(processedItems);
        }

        // GET: Process/Create - Select parent and add children
        public async Task<IActionResult> Create()
        {
            var availableItems = await _context.Items
                .Where(i => !i.IsProcessed)
                .OrderBy(i => i.Name)
                .ToListAsync();

            var model = new ProcessItemViewModel
            {
                AvailableItems = availableItems,
                ChildItems = new List<ChildItemInput> { new ChildItemInput() }
            };

            return View(model);
        }

        // POST: Process/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(ProcessItemViewModel model)
        {
            // Remove null/empty child items before validation
            model.ChildItems = model.ChildItems
                .Where(c => !string.IsNullOrWhiteSpace(c.Name))
                .ToList();

            if (!model.ChildItems.Any())
                ModelState.AddModelError("ChildItems", "At least one child item is required.");

            if (!ModelState.IsValid)
            {
                model.AvailableItems = await _context.Items
                    .Where(i => !i.IsProcessed)
                    .OrderBy(i => i.Name)
                    .ToListAsync();
                return View(model);
            }

            var parentItem = await _context.Items.FindAsync(model.ParentItemId);
            if (parentItem == null)
            {
                ModelState.AddModelError("ParentItemId", "Selected parent item not found.");
                model.AvailableItems = await _context.Items
                    .Where(i => !i.IsProcessed)
                    .OrderBy(i => i.Name)
                    .ToListAsync();
                return View(model);
            }

            // Mark parent as processed
            parentItem.IsProcessed = true;
            parentItem.UpdatedAt = DateTime.UtcNow;

            // Create child items
            foreach (var child in model.ChildItems)
            {
                var childItem = new Item
                {
                    Name = child.Name.Trim(),
                    Weight = child.Weight,
                    Description = child.Description?.Trim(),
                    ParentItemId = parentItem.Id,
                    IsProcessed = false,
                    CreatedAt = DateTime.UtcNow
                };
                _context.Items.Add(childItem);
            }

            await _context.SaveChangesAsync();
            TempData["Success"] = $"Item '{parentItem.Name}' processed successfully with {model.ChildItems.Count} child item(s).";
            return RedirectToAction(nameof(Index));
        }

        // GET: Process/Tree - Full tree view
        public async Task<IActionResult> Tree()
        {
            var allItems = await _context.Items
                .Include(i => i.ChildItems)
                .ToListAsync();

            // Build tree starting from root nodes (no parent)
            var roots = allItems
                .Where(i => i.ParentItemId == null)
                .Select(i => BuildTreeNode(i, allItems))
                .OrderBy(n => n.Name)
                .ToList();

            return View(roots);
        }

        // GET: Process/ItemTree/5 - Tree view for a specific item
        public async Task<IActionResult> ItemTree(int id)
        {
            var allItems = await _context.Items
                .Include(i => i.ChildItems)
                .ToListAsync();

            var rootItem = allItems.FirstOrDefault(i => i.Id == id);
            if (rootItem == null)
                return NotFound();

            var treeNode = BuildTreeNode(rootItem, allItems);
            return View(treeNode);
        }

        private TreeNodeViewModel BuildTreeNode(Item item, List<Item> allItems)
        {
            var node = new TreeNodeViewModel
            {
                Id = item.Id,
                Name = item.Name,
                Weight = item.Weight,
                IsProcessed = item.IsProcessed,
                ParentItemId = item.ParentItemId,
                Children = allItems
                    .Where(c => c.ParentItemId == item.Id)
                    .Select(c => BuildTreeNode(c, allItems))
                    .OrderBy(c => c.Name)
                    .ToList()
            };
            return node;
        }
    }
}
