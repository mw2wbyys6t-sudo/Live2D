#!/bin/bash
# 测试网络稳定性的脚本

echo "======================================================================"
echo "🌐 Live2D Master Agent - 网络稳定性测试"
echo "======================================================================"
echo ""

echo "1. 检查 Python 版本..."
python3 --version
echo ""

echo "2. 测试网络连接..."
python3 << 'PYEOF'
import socket
import urllib.request

print("   🔍 检查 DNS 解析...")
try:
    ip = socket.gethostbyname("pollinations.ai")
    print(f"   ✅ DNS 解析成功: {ip}")
except Exception as e:
    print(f"   ❌ DNS 解析失败: {e}")

print("\n   🔍 检查 Pollinations.ai...")
try:
    req = urllib.request.Request("https://image.pollinations.ai", method='HEAD')
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib.request.urlopen(req, timeout=10)
    print(f"   ✅ Pollinations.ai 可访问 (状态码: {response.status})")
except Exception as e:
    print(f"   ⚠️ Pollinations.ai 暂时不可用: {e}")

print("\n   🔍 检查 Hugging Face...")
try:
    req = urllib.request.Request("https://api-inference.huggingface.co", method='HEAD')
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib.request.urlopen(req, timeout=10)
    print(f"   ✅ Hugging Face 可访问 (状态码: {response.status})")
except Exception as e:
    print(f"   ⚠️ Hugging Face 暂时不可用: {e}")

print("\n" + "=" * 70)
print("✅ 网络检查完成")
print("=" * 70)
PYEOF

echo ""
echo "💡 提示: 如果网络暂时不稳定，工具会自动重试最多 3 次"
echo "======================================================================"
