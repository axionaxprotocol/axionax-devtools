# Axionax Protocol - Refactoring & Code Quality Tools

เครื่องมือสำหรับ refactor และปรับปรุงคุณภาพของ code ทั้ง Axionax Protocol

## 📚 สคริปท์ที่มีให้ใช้

### 1. 🏥 `check_repo_health.py` - Repository Health Checker
ตรวจสอบสุขภาพของ repositories ทั้งหมด

**การใช้งาน:**
```bash
python check_repo_health.py
```

**ตรวจสอบ:**
- ✅ .gitignore ครบถ้วนหรือไม่
- ✅ ไฟล์ที่ยังไม่ commit
- ✅ package-lock.json
- ✅ dependency versions
- ✅ README.md

---

### 2. 🔗 `test_repo_links.py` - Repository Link Tester
ทดสอบการลิงค์ระหว่าง repositories

**การใช้งาน:**
```bash
python test_repo_links.py
```

**ตรวจสอบ:**
- ✅ file: links ถูกต้องหรือไม่
- ✅ dependencies ระหว่าง repos
- ✅ import resolution
- ❌ ไม่ใช้ workspace: protocol
- ❌ ไม่ลิงค์ผ่าน contributors

---

### 3. 🔍 `analyze_code_quality.py` - Code Quality Analyzer
วิเคราะห์คุณภาพของ code อย่างละเอียด

**การใช้งาน:**
```bash
python analyze_code_quality.py
```

**วิเคราะห์:**

#### TypeScript/JavaScript:
- ⚠️ ฟังก์ชันยาวเกินไป (>50 บรรทัด)
- ⚠️ Magic numbers
- ⚠️ Nested if statements (>3 levels)
- ⚠️ TODO/FIXME comments
- ⚠️ Commented code
- ⚠️ `any` types
- ⚠️ Empty catch blocks

#### Rust:
- ⚠️ `.unwrap()` และ `.expect()` มากเกินไป
- ⚠️ `.clone()` มากเกินไป
- ⚠️ `unsafe` blocks
- ⚠️ Public items ไม่มี documentation
- ⚠️ TODO/FIXME comments

---

### 4. 🧹 `refactor_and_clean.py` - Refactor & Clean Tool
ทำความสะอาดและ refactor code อัตโนมัติ

**การใช้งาน:**
```bash
# รัน refactor ทั้งหมด
python refactor_and_clean.py

# ข้ามการ format
python refactor_and_clean.py --skip-formatting

# ข้ามการ lint
python refactor_and_clean.py --skip-linting

# Refactor เฉพาะ repo
python refactor_and_clean.py --repo axionax-core
```

**ทำอะไรบ้าง:**

#### ทุก Repo:
1. ✅ สร้าง/อัพเดท .gitignore
2. ✅ ตรวจหาไฟล์ที่ไม่ได้ใช้
3. ✅ ตรวจสอบ documentation

#### TypeScript Repos:
1. ✅ ลบ `console.log()` ที่เหลือค้าง
2. ✅ ลบ `debugger` statements
3. ✅ ลบ empty lines ที่ซ้อนกัน
4. ✅ ลบ trailing whitespace
5. ✅ รัน Prettier (ถ้ามี)
6. ✅ รัน ESLint --fix (ถ้ามี)

#### Rust Repos:
1. ✅ ลบ empty lines ที่ซ้อนกัน
2. ✅ ลบ trailing whitespace
3. ✅ รัน rustfmt
4. ✅ รัน clippy --fix

---

### 5. ✅ `test_repo_integration.py` - Integration Tester
ทดสอบการเชื่อมต่อและความพร้อมของทุก repo

**การใช้งาน:**
```bash
python test_repo_integration.py
```

**ทดสอบ:**
- ✅ Repository existence
- ✅ Git status
- ✅ Package/Cargo validation
- ✅ Dependencies
- ✅ Build system
- ✅ Import resolution

---

### 6. 🚀 `master_refactor.py` - Master Script
รันทุกสคริปท์ตามลำดับในคำสั่งเดียว

**การใช้งาน:**
```bash
python master_refactor.py
```

**ลำดับการทำงาน:**
1. 📋 Health Check
2. 🔗 Link Testing
3. 🔍 Code Quality Analysis
4. 🧹 Refactor & Clean
5. ✅ Final Integration Test

---

## 🎯 Workflow แนะนำ

### สำหรับการพัฒนาประจำวัน:
```bash
# 1. ตรวจสอบสุขภาพ
python check_repo_health.py

# 2. ทำความสะอาด code
python refactor_and_clean.py

# 3. ทดสอบ
python test_repo_integration.py
```

### สำหรับการปรับปรุงคุณภาพ code:
```bash
# 1. วิเคราะห์คุณภาพ
python analyze_code_quality.py

# 2. ดู issues ที่พบ
# 3. แก้ไข manual
# 4. รัน refactor
python refactor_and_clean.py

# 5. ทดสอบอีกครั้ง
python test_repo_integration.py
```

### สำหรับ Full Refactor:
```bash
# รันทุกอย่างพร้อมกัน
python master_refactor.py
```

---

## 📊 ผลลัพธ์ที่ได้

หลังจากรันสคริปท์เหล่านี้ คุณจะได้:

1. **Code ที่สะอาด:**
   - ✅ ไม่มี console.log/debugger
   - ✅ ไม่มี trailing whitespace
   - ✅ Format สม่ำเสมอ
   - ✅ Lint errors น้อยลง

2. **.gitignore ที่ถูกต้อง:**
   - ✅ Ignore ไฟล์ที่ไม่ต้องการทั้งหมด
   - ✅ แยกตามประเภท repo

3. **Dependencies ที่ชัดเจน:**
   - ✅ ใช้ file: links
   - ✅ ไม่ลิงค์ผ่าน workspace
   - ✅ Resolve ได้ทุก repo

4. **Documentation:**
   - ✅ README.md ครบถ้วน
   - ✅ Code comments เหมาะสม
   - ✅ ไม่มี TODO เก่าๆ

5. **รายงานครบถ้วน:**
   - 📄 `REPO_LINK_TEST_REPORT.txt`
   - 📄 `INTEGRATION_TEST_REPORT.txt`
   - 📄 `integration_test_results.json`

---

## ⚙️ Configuration

### Prettier (TypeScript)
สร้างไฟล์ `.prettierrc` ใน repo:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### ESLint (TypeScript)
ใช้ config ที่มีอยู่แล้วใน `package.json` หรือสร้าง `.eslintrc.json`

### rustfmt (Rust)
สร้างไฟล์ `rustfmt.toml` ใน repo:
```toml
max_width = 100
hard_tabs = false
tab_spaces = 4
edition = "2021"
```

---

## 🚨 คำเตือน

1. **Backup ก่อนรัน:**
   ```bash
   git add -A
   git commit -m "backup before refactor"
   ```

2. **ตรวจสอบการเปลี่ยนแปลง:**
   ```bash
   git diff
   ```

3. **ทดสอบหลังแก้ไข:**
   ```bash
   # TypeScript
   npm test
   npm run build
   
   # Rust
   cargo test
   cargo build
   ```

4. **อย่าลืม commit:**
   ```bash
   git add -A
   git commit -m "refactor: improve code quality"
   git push
   ```

---

## 🤝 Contributing

หากพบปัญหาหรือต้องการเพิ่ม feature:

1. Fork repository
2. สร้าง branch ใหม่
3. ทำการเปลี่ยนแปลง
4. รัน `python master_refactor.py`
5. Submit Pull Request

---

## 📝 License

MIT License - ดูที่ LICENSE file

---

## 🎉 Happy Refactoring!

Made with ❤️ for Axionax Protocol
