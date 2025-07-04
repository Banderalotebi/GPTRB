#!/bin/bash

# نسخ ملفات من سطح المكتب إلى مجلد المشروع
# Copy files from desktop to project folder

echo "🗂️  نسخ ملفات النصوص من سطح المكتب"
echo "Copying text files from desktop"
echo "================================="

# محاولة العثور على مجلد سطح المكتب
# Try to find desktop folder
DESKTOP_PATHS=(
    "$HOME/Desktop"
    "$HOME/سطح المكتب"
    "/mnt/c/Users/$USER/Desktop"  # WSL
    "/home/$USER/Desktop"
)

DESKTOP_PATH=""
for path in "${DESKTOP_PATHS[@]}"; do
    if [ -d "$path" ]; then
        DESKTOP_PATH="$path"
        echo "✅ وُجد مجلد سطح المكتب: $DESKTOP_PATH"
        break
    fi
done

if [ -z "$DESKTOP_PATH" ]; then
    echo "❌ لم يُعثر على مجلد سطح المكتب"
    echo "Please specify desktop path manually:"
    read -p "مسار سطح المكتب: " DESKTOP_PATH
    
    if [ ! -d "$DESKTOP_PATH" ]; then
        echo "❌ المسار غير موجود"
        exit 1
    fi
fi

# إنشاء مجلد البيانات
# Create data directory
mkdir -p training_data

# البحث عن الملفات النصية
# Find text files
echo ""
echo "🔍 البحث عن الملفات النصية..."
echo "Looking for text files..."

# نسخ الملفات النصية
# Copy text files
COPIED=0
for ext in txt md csv json tsv; do
    for file in "$DESKTOP_PATH"/*.$ext; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            cp "$file" "training_data/$filename"
            echo "✅ تم نسخ: $filename"
            ((COPIED++))
        fi
    done
done

if [ $COPIED -eq 0 ]; then
    echo "❌ لم يُعثر على ملفات نصية في سطح المكتب"
    echo "No text files found on desktop"
else
    echo ""
    echo "🎉 تم نسخ $COPIED ملف إلى training_data/"
    echo "Copied $COPIED files to training_data/"
    
    echo ""
    echo "📋 الملفات المنسوخة:"
    echo "Copied files:"
    ls -la training_data/
    
    echo ""
    echo "🚀 الخطوة التالية:"
    echo "Next step:"
    echo "python3 text_data_processor.py"
fi
