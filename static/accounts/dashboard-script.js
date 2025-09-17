console.log("hello")
console.log("hello")
$(document).ready(function() {
    // Toggle sidebar on small screens
    $('#sidebarToggle').click(function() {
        $('body').toggleClass('sidebar-toggled');
        $('.sidebar').toggleClass('toggled');
    });

    // Close sidebar when clicking outside on mobile
    $(document).click(function(e) {
        if ($(window).width() < 768) {
            if (!$('.sidebar').is(e.target) && $('.sidebar').has(e.target).length === 0 && $('.sidebar').hasClass('toggled')) {
                $('body').removeClass('sidebar-toggled');
                $('.sidebar').removeClass('toggled');
            }
        }
    });

    // Prevent dropdown from closing when clicking inside
    $('.dropdown-menu').on('click', function(e) {
        e.stopPropagation();
    });

    // Handle quick action buttons based on their IDs
    $('#uploadResumeBtn').click(function() {
        console.log('Upload Resume functionality would be implemented here.');
        // Add your resume upload logic
        const postJobUrl = $(this).data('url')

        if (postJobUrl){
            window.location.href = postJobUrl;
        }  else {
            console.error('Job posting Url not found')
        }
    });

    $('#postJobBtn').click(function() {
        console.log('Post a Job functionality would be implemented here.');
        // logic
        const postJobUrl = $(this).data('url')

        if (postJobUrl){
            window.location.href = postJobUrl;
        }  else {
            console.error('Job posting Url not found')
        }
    });

    $('#viewAllBtn').click(function() {
        console.log('View All functionality would be implemented here.');
        // Add your view all logic
    });

    // Handle view resume buttons (placeholder)
    $('.btn-outline-primary').click(function() {
        const candidateName = $(this).closest('tr').find('td:first').text();
        console.log(`Viewing resume for: ${candidateName}`);
    });

    // Handle search functionality
    function handleSearch(query) {
        // This would be replaced with actual search implementation
        console.log(`Searching for: ${query}`);
    }

    // Handle filter changes
    function handleFilterChange(filterType, value) {
        // This would be replaced with actual filter implementation
        console.log(`Filter changed: ${filterType} = ${value}`);
    }

    // Export data function
    function exportData(format) {
        // This would be replaced with actual export implementation
        console.log(`Exporting data in ${format} format`);
    }
});
