using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ADMS.ERP.Data;
using ADMS.ERP.Models;

namespace ADMS.ERP.Controllers
{
    [Authorize]
    public class ItemController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ItemController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: Item (List with optional search)
        public async Task<IActionResult> Index(string? search)
        {
            ViewData["CurrentSearch"] = search;
            var query = _context.Items
                .Include(i => i.ParentItem)
                .AsQueryable();

            if (!string.IsNullOrWhiteSpace(search))
            {
                query = query.Where(i =>
                    i.Name.Contains(search) ||
                    (i.Description != null && i.Description.Contains(search)));
            }

            var items = await query.OrderBy(i => i.Name).ToListAsync();
            return View(items);
        }

        // GET: Item/Details/5
        public async Task<IActionResult> Details(int id)
        {
            var item = await _context.Items
                .Include(i => i.ParentItem)
                .Include(i => i.ChildItems)
                .FirstOrDefaultAsync(i => i.Id == id);

            if (item == null)
                return NotFound();

            return View(item);
        }

        // GET: Item/Create
        public IActionResult Create()
        {
            return View(new Item());
        }

        // POST: Item/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Item item)
        {
            if (!ModelState.IsValid)
                return View(item);

            item.CreatedAt = DateTime.UtcNow;
            _context.Items.Add(item);
            await _context.SaveChangesAsync();
            TempData["Success"] = $"Item '{item.Name}' created successfully.";
            return RedirectToAction(nameof(Index));
        }

        // GET: Item/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            var item = await _context.Items.FindAsync(id);
            if (item == null)
                return NotFound();

            return View(item);
        }

        // POST: Item/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Item item)
        {
            if (id != item.Id)
                return BadRequest();

            if (!ModelState.IsValid)
                return View(item);

            var existing = await _context.Items.FindAsync(id);
            if (existing == null)
                return NotFound();

            existing.Name = item.Name;
            existing.Weight = item.Weight;
            existing.Description = item.Description;
            existing.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();
            TempData["Success"] = $"Item '{existing.Name}' updated successfully.";
            return RedirectToAction(nameof(Index));
        }

        // GET: Item/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            var item = await _context.Items
                .Include(i => i.ChildItems)
                .FirstOrDefaultAsync(i => i.Id == id);

            if (item == null)
                return NotFound();

            return View(item);
        }

        // POST: Item/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var item = await _context.Items
                .Include(i => i.ChildItems)
                .FirstOrDefaultAsync(i => i.Id == id);

            if (item == null)
                return NotFound();

            if (item.ChildItems.Any())
            {
                TempData["Error"] = "Cannot delete an item that has child items. Please delete child items first.";
                return RedirectToAction(nameof(Index));
            }

            _context.Items.Remove(item);
            await _context.SaveChangesAsync();
            TempData["Success"] = $"Item '{item.Name}' deleted successfully.";
            return RedirectToAction(nameof(Index));
        }
    }
}
