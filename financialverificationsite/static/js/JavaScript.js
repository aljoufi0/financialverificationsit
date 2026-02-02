// --- 1. وظائف القوائم المنسدلة (Navbar) ---
function toggleMenu(menuId, event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault(); // منع السلوك الافتراضي للرابط
    }
    
    // إغلاق أي قائمة أخرى مفتوحة
    document.querySelectorAll('.dropdown-content').forEach(menu => {
        if (menu.id !== menuId) menu.classList.remove('show');
    });

    // تبديل حالة القائمة المطلوبة
    const targetMenu = document.getElementById(menuId);
    if (targetMenu) {
        targetMenu.classList.toggle('show');
    }
}

// إغلاق القوائم عند الضغط خارجها
window.onclick = function(event) {
    if (!event.target.matches('.drop-trigger')) {
        document.querySelectorAll('.dropdown-content').forEach(menu => {
            menu.classList.remove('show');
        });
    }
}

// --- 2. وظيفة الطباعة الخاصة بالتقارير ---
function doPrint() {
    const dateElement = document.getElementById('p-date');
    if (dateElement) {
        // تحديث تاريخ التقرير تلقائياً عند الضغط على طباعة
        dateElement.innerText = new Date().toLocaleDateString('ar-YE');
    }
    window.print();
}

// --- 3. كود تحريك الصور المتقلبة (Slider) ---
let currentSlide = 0;

function moveSlide(step) {
    const slidesContainer = document.getElementById('slides');
    const dots = document.querySelectorAll('.dot'); 
    const slides = document.querySelectorAll('.slide');
    
    if (!slidesContainer || slides.length === 0) return; // تأمين الكود في حال لم يكن بالرئيسية

    const totalSlides = slides.length;
    
    // تحديث المؤشر الحالي
    currentSlide = (currentSlide + step + totalSlides) % totalSlides;
    
    // تحريك الصور (وضع RTL)
    const offset = currentSlide * 100;
    slidesContainer.style.transform = `translateX(${offset}%)`;

    // تحديث حالة النقاط
    dots.forEach((dot, index) => {
        if (index === currentSlide) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

// دالة للانتقال مباشرة لصورة معينة عند الضغط على نقطة
function currentSlideAction(index) {
    manualMove(index - currentSlide);
}

// التحريك التلقائي كل 5 ثواني
let sliderTimer = setInterval(() => {
    if (document.getElementById('slides')) moveSlide(1);
}, 5000);

// التحريك اليدوي (يصفر العداد)
function manualMove(step) {
    clearInterval(sliderTimer);
    moveSlide(step);
    sliderTimer = setInterval(() => moveSlide(1), 5000);
}

// --- 4. وظيفة تأكيد تسجيل الخروج ---
// تم تعديل الكود ليعمل بشكل آمن حتى لو لم يكن الزر موجوداً في الصفحة
document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('logout-btn')) {
        const confirmation = confirm("هل أنت متأكد من رغبتك في تسجيل الخروج؟");
        if (!confirmation) {
            e.preventDefault();
        }
    }
});

