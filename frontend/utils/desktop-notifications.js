// Desktop Notifications Manager
class DesktopNotifications {
    constructor() {
        this.permission = Notification.permission;
        this.enabled = localStorage.getItem('desktopNotificationsEnabled') === 'true';
    }

    async requestPermission() {
        if (!('Notification' in window)) {
            console.warn('Desktop notifications not supported');
            return false;
        }
        
        if (this.permission === 'granted') {
            this.enabled = true;
            localStorage.setItem('desktopNotificationsEnabled', 'true');
            return true;
        }
        
        const permission = await Notification.requestPermission();
        this.permission = permission;
        
        if (permission === 'granted') {
            this.enabled = true;
            localStorage.setItem('desktopNotificationsEnabled', 'true');
            return true;
        }
        
        return false;
    }

    notify(title, options = {}) {
        if (!this.enabled || this.permission !== 'granted') return;
        
        const notification = new Notification(title, {
            icon: '/favicon.ico',
            badge: '/favicon.ico',
            ...options
        });
        
        notification.onclick = () => {
            window.focus();
            notification.close();
        };
        
        setTimeout(() => notification.close(), 5000);
    }

    toggle() {
        if (!this.enabled && this.permission !== 'granted') {
            return this.requestPermission();
        }
        
        this.enabled = !this.enabled;
        localStorage.setItem('desktopNotificationsEnabled', this.enabled);
        return Promise.resolve(this.enabled);
    }

    isEnabled() {
        return this.enabled && this.permission === 'granted';
    }
}

export default new DesktopNotifications();
