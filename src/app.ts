import { initNavbar } from './include/ui/navbar/navbar';
import Alpine from 'alpinejs';
import PineconeRouter from 'pinecone-router';


document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
});

declare global {
    interface Window {
        Alpine: Alpine;
    }
}

window.Alpine = Alpine;
Alpine.plugin(PineconeRouter)
Alpine.start();
