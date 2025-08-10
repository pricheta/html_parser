SET_PROXY_LOCATION_SCRIPT = \
"""
window._realLocation = null;

window._originalAssign = window.location.assign;
window._originalReplace = window.location.replace;

window.location.assign = function(url) {
    window._realLocation = url;
};

window.location.replace = function(url) {
    window._realLocation = url;
};
"""

GET_CLICKED_BLOCK_URL_SCRIPT = \
"""
function interceptClickAndGetUrl(element) {
    return new Promise((resolve) => {
        const originalHref = element.href || element.getAttribute('data-href') || null;
        let interceptedUrl = null;

        const clickHandler = (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            interceptedUrl = originalHref;
        };
        element.addEventListener('click', clickHandler, { capture: true, once: true });

        const urlBeforeClick = window.location.href;

        element.click();

        setTimeout(() => {
            if (window.location.href !== urlBeforeClick) {
                interceptedUrl = window.location.href;
                window.history.back();  
            }
            resolve(interceptedUrl || originalHref);
        }, 500);
    });
}

return interceptClickAndGetUrl(arguments[0]);
"""
