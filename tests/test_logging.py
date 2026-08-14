import logging

# 配置日志
# level=logging.INFO 表示只显示INFO级别及以上的日志
# format 定义了日志的输出格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 获取logger实例
logger = logging.getLogger(__name__)

# 测试各种级别的日志
logger.debug("这是DEBUG级别的日志 - 不会显示")
logger.info("这是INFO级别的日志 - 会显示 ✅")
logger.warning("这是WARNING级别的日志 - 会显示 ⚠️")
logger.error("这是ERROR级别的日志 - 会显示 ❌")
logger.critical("这是CRITICAL级别的日志 - 会显示 🔥")

# 更复杂的测试
def test_function():
    logger.info("进入测试函数")
    try:
        result = 10 / 2
        logger.info(f"计算结果: {result}")
        return result
    except Exception as e:
        logger.error(f"发生错误: {e}")

# 调用函数
test_function()

logger.info("日志测试完成!")