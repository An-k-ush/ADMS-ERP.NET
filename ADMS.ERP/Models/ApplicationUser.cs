using Microsoft.AspNetCore.Identity;

namespace ADMS.ERP.Models
{
    public class ApplicationUser : IdentityUser
    {
        public string FullName { get; set; } = string.Empty;
    }
}
