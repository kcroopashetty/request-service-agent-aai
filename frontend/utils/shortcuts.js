// Keyboard Shortcuts
export function setupKeyboardShortcuts(handlers) {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K: Focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            handlers.focusSearch?.();
        }
        
        // Ctrl/Cmd + N: New request
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            handlers.newRequest?.();
        }
        
        // Ctrl/Cmd + E: Export
        if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
            e.preventDefault();
            handlers.export?.();
        }
        
        // Ctrl/Cmd + D: Toggle theme
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            handlers.toggleTheme?.();
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            handlers.closeModal?.();
        }
    });
}
