import Alpine from 'alpinejs';

declare global {
    interface Window {
        Alpine: Alpine;
    }
}

window.Alpine = Alpine;
Alpine.start();
