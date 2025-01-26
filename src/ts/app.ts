import { initNavbar } from './ui/navbar/navbar';
import Alpine from 'alpinejs';

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
});

declare global {
    interface Window {
        Alpine: Alpine;
    }
}

window.Alpine = Alpine;
Alpine.start();
