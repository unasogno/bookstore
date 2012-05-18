# -*- coding:utf8 -*-

from multiprocessing import Process
import config
import handler
import helpers

if __name__ == '__main__':
  logger = helpers.init_logger('loader', config.LOG_PATH)
  for handler_config in config.HANDLER_CONFIG:
    try:
      exec 'import ' + handler_config.module_name
      process = Process(
        target = handler.run,
        name = handler_config.module_name,
        args = (
          handler_config.send_spec, 
          handler_config.recv_spec, 
          handler.handlers_registry[
            handler_config.module_name]))
      logger.info('starting %s', process.name)
      process.start()
      logger.info('process %d started', process.pid)
    except:
      logger.error(helpers.format_exception())
