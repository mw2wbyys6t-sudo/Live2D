from playwright.sync_api import sync_playwright
import json
import os

BASE_URL = 'http://localhost:3000/Live2D'
REPORT = []

def log(section, status, detail):
    REPORT.append({'section': section, 'status': status, 'detail': detail})
    icon = '✅' if status == 'PASS' else '⚠️' if status == 'WARN' else '❌'
    print(f'  {icon} [{status}] {section}: {detail}')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    page.on('console', lambda msg: log(f'Console [{msg.type}]', 'WARN' if msg.type == 'error' else 'INFO', msg.text))
    page.on('pageerror', lambda err: log('Page Error', 'FAIL', str(err)))

    print('\n=== 1. 页面加载测试 ===')
    page.goto(BASE_URL, wait_until='networkidle', timeout=15000)
    log('首页加载', 'PASS', f'状态码 200, URL: {page.url}')

    title = page.title()
    log('页面标题', 'PASS', f'"{title}"')

    html = page.content()
    log('HTML 渲染', 'PASS', f'页面大小: {len(html)} 字符')

    print('\n=== 2. UI 结构检查 ===')
    header = page.locator('header')
    log('Header 存在', 'PASS' if header.count() > 0 else 'FAIL', f'找到 {header.count()} 个 header')

    main = page.locator('main')
    log('Main 存在', 'PASS' if main.count() > 0 else 'FAIL', f'找到 {main.count()} 个 main')

    h1 = page.locator('h1')
    log('H1 标题', 'PASS' if h1.count() > 0 else 'FAIL', f'文本: "{h1.first.text_content()}"')

    tabs = page.locator('header button')
    tab_count = tabs.count()
    log('导航按钮', 'PASS' if tab_count >= 2 else 'WARN', f'找到 {tab_count} 个按钮')

    print('\n=== 3. 模式切换测试 ===')
    psd_tab = page.locator('button', has_text='PSD 检测')
    convert_tab = page.locator('button', has_text='图片转PSD')
    log('PSD检测标签', 'PASS' if psd_tab.count() > 0 else 'FAIL', f'可见: {psd_tab.is_visible()}')
    log('图片转PSD标签', 'PASS' if convert_tab.count() > 0 else 'FAIL', f'可见: {convert_tab.is_visible()}')

    psd_tab.click()
    page.wait_for_timeout(500)
    log('PSD模式切换', 'PASS', '点击 PSD 检测标签')

    convert_tab.click()
    page.wait_for_timeout(500)
    log('图片转PSD模式切换', 'PASS', '点击 图片转PSD 标签')

    convert_section = page.locator('text=图片转 PSD')
    log('转换页面渲染', 'PASS' if convert_section.count() > 0 else 'FAIL', f'可见: {convert_section.is_visible()}')

    print('\n=== 4. 图片转PSD功能检查 ===')
    upload_area = page.locator('text=上传图片文件')
    log('上传区域', 'PASS' if upload_area.count() > 0 else 'FAIL', f'可见: {upload_area.is_visible()}')

    feature_items = page.locator('text=一键转换')
    log('功能说明', 'PASS' if feature_items.count() > 0 else 'FAIL', '一键转换功能说明')

    file_input = page.locator('input[type="file"]')
    log('文件输入', 'PASS' if file_input.count() > 0 else 'FAIL', f'accept: {file_input.get_attribute("accept")}')

    print('\n=== 5. 页面截图 ===')
    screenshot_dir = '/tmp/analysis'
    os.makedirs(screenshot_dir, exist_ok=True)

    convert_tab.click()
    page.wait_for_timeout(300)
    page.screenshot(path=f'{screenshot_dir}/01-convert-mode.png', full_page=True)
    log('截图: 转换模式', 'PASS', f'saved to {screenshot_dir}/01-convert-mode.png')

    psd_tab.click()
    page.wait_for_timeout(300)
    page.screenshot(path=f'{screenshot_dir}/02-psd-qa-mode.png', full_page=True)
    log('截图: PSD检测模式', 'PASS', f'saved to {screenshot_dir}/02-psd-qa-mode.png')

    print('\n=== 6. 响应式布局检查 ===')
    for vp_name, vp_size in [('手机 375x812', {'width': 375, 'height': 812}), ('平板 768x1024', {'width': 768, 'height': 1024})]:
        vp_context = browser.new_context(viewport=vp_size)
        vp_page = vp_context.new_page()
        vp_page.goto(BASE_URL, wait_until='networkidle', timeout=10000)
        vp_page.wait_for_timeout(500)
        vp_page.screenshot(path=f'{screenshot_dir}/responsive-{vp_name.split()[0]}.png', full_page=True)

        header_visible = vp_page.locator('h1').is_visible()
        upload_visible = vp_page.locator('text=上传 PSD 文件').is_visible()
        log(f'响应式 {vp_name}', 'PASS' if upload_visible else 'WARN',
            f'标题可见:{header_visible}, 上传区域可见:{upload_visible}')
        vp_context.close()

    print('\n=== 7. Console 日志分析 ===')
    errors = []
    for entry in REPORT:
        if entry['status'] == 'FAIL' or (entry['section'].startswith('Console') and 'error' in entry['detail'].lower()):
            errors.append(entry)
    log('错误日志', 'PASS' if len(errors) == 0 else 'WARN', f'共 {len(errors)} 个错误')

    browser.close()

    print('\n' + '=' * 60)
    print('📊 综合分析报告')
    print('=' * 60)

    total = len(REPORT)
    passed = sum(1 for r in REPORT if r['status'] == 'PASS')
    warned = sum(1 for r in REPORT if r['status'] == 'WARN')
    failed = sum(1 for r in REPORT if r['status'] == 'FAIL')

    print(f'\n总计: {total} 项检查 | ✅ {passed} 通过 | ⚠️ {warned} 警告 | ❌ {failed} 失败')
    print(f'\n截图已保存至: {screenshot_dir}/')

    if warned > 0 or failed > 0:
        print('\n需要关注的问题:')
        for r in REPORT:
            if r['status'] in ('WARN', 'FAIL'):
                print(f'  [{r["status"]}] {r["section"]}: {r["detail"]}')