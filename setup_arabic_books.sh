#!/bin/bash

# إعداد سريع للكتب العربية
# Quick setup for Arabic books

echo "📚 إعداد معالج الكتب العربية"
echo "Setting up Arabic Books Processor"
echo "=================================="

# تثبيت المكتبات المطلوبة
echo "📦 Installing required packages..."
pip install arabic-reshaper python-bidi PyPDF2 python-docx openpyxl

# إنشاء مجلدات البيانات
echo "📁 Creating data directories..."
mkdir -p training_data
mkdir -p models

# التحقق من وجود git
if ! command -v git &> /dev/null; then
    echo "⚠️ Git is not installed. Please install git to clone repositories."
else
    echo "✅ Git is available"
fi

# استنساخ مستودع الكتب العربية
echo "📥 Cloning Arabic books repository..."
if [ ! -d "arb" ]; then
    echo "Trying HTTPS clone..."
    git clone https://github.com/Banderalotebi/arb.git || {
        echo "HTTPS failed, trying SSH..."
        git clone git@github.com:Banderalotebi/arb.git || {
            echo "❌ Failed to clone repository. You can download it manually."
        }
    }
else
    echo "✅ Repository already exists"
fi

# إنشاء ملفات نموذجية إذا لم توجد كتب
if [ ! -d "arb" ] && [ ! -d "desktop/training" ] && [ ! -d "Desktop/training" ]; then
    echo "📝 Creating sample Arabic texts..."
    
    cat > training_data/sample_arabic_1.txt << 'EOF'
الذكاء الاصطناعي والتعلم الآلي

الذكاء الاصطناعي هو مجال واسع في علوم الحاسوب يهدف إلى إنشاء أنظمة قادرة على أداء مهام تتطلب عادة ذكاءً بشرياً. يشمل هذا المجال العديد من التقنيات والأساليب مثل التعلم الآلي، ومعالجة اللغات الطبيعية، والرؤية الحاسوبية، والروبوتات.

التعلم الآلي هو فرع من فروع الذكاء الاصطناعي يركز على تطوير خوارزميات وأساليب إحصائية تمكن أجهزة الحاسوب من التعلم وتحسين أدائها في مهمة معينة من خلال الخبرة والبيانات، دون الحاجة إلى برمجة صريحة لكل حالة.

تطبيقات الذكاء الاصطناعي في حياتنا اليومية متعددة ومتنوعة، من محركات البحث على الإنترنت إلى أنظمة التوصية في منصات التجارة الإلكترونية والترفيه، ومن المساعدات الصوتية الذكية إلى أنظمة القيادة الذاتية في السيارات.

أما التحديات التي يواجهها الذكاء الاصطناعي فتشمل قضايا الأخلاق والخصوصية، والحاجة إلى كميات كبيرة من البيانات، وضرورة ضمان الشفافية والقابلية للتفسير في القرارات التي تتخذها الأنظمة الذكية.
EOF

    cat > training_data/sample_arabic_2.txt << 'EOF'
البرمجة وتطوير البرمجيات

البرمجة هي عملية إنشاء وتصميم وبناء برامج الحاسوب باستخدام لغات البرمجة المختلفة. تهدف البرمجة إلى حل المشكلات وتنفيذ المهام من خلال كتابة مجموعة من التعليمات والأوامر التي يفهمها الحاسوب.

لغات البرمجة متنوعة ومتعددة، كل منها له خصائصه ومجالات استخدامه. من أشهر لغات البرمجة: Python للذكاء الاصطناعي وتحليل البيانات، JavaScript لتطوير المواقع، Java لتطوير التطبيقات المؤسسية، C++ للبرمجة النظمية وألعاب الفيديو.

عملية تطوير البرمجيات تمر بمراحل عديدة تشمل: تحليل المتطلبات، التصميم، التنفيذ، الاختبار، النشر، والصيانة. كل مرحلة من هذه المراحل لها أهميتها ودورها في ضمان جودة المنتج النهائي.

مستقبل البرمجة يتجه نحو المزيد من التخصص والتطور، مع ظهور تقنيات جديدة مثل الحوسبة السحابية، إنترنت الأشياء، والواقع المعزز، مما يفتح آفاقاً جديدة للمبرمجين والمطورين.
EOF

    echo "✅ Sample Arabic texts created"
fi

echo ""
echo "🎯 الإعداد مكتمل! يمكنك الآن:"
echo "Setup complete! You can now:"
echo "1. Run: python3 arabic_books_processor.py"
echo "2. Or: python3 llama_finetuning.py"
echo ""
echo "📋 للحصول على مساعدة سريعة:"
echo "python3 arabic_books_processor.py --help"
