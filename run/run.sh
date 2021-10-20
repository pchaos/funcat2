#!/bin/bash
# 自用
# 10日卡夫曼自适应均线选股
funcatenv="funcat"
if [ $CONDA_DEFAULT_ENV != "${funcatenv}" ]; then
  echo "not in env ${funcatenv}"

  FILE=~/.bashrc
  if test -f "$FILE"; then
      # echo "$FILE exists."
      . $FILE
      conda activate funcat
      echo conda env $CONDA_DEFAULT_ENV
  fi
fi
testfile=tests/funcat/test_ema_trends.py
if [ -f ${testfile} ] ;then 
  pytest -v  "${testfile}"::Test_ema_trend::test_condition_kama_ema3
else
  pytest -v  "../${testfile}"::Test_ema_trend::test_condition_kama_ema3
fi
conda deactivate
echo conda env $CONDA_DEFAULT_ENV
FILE=/tmp/kama*.txt
# [ -n"$(find /tmp -name '${FILE}' | head -1)" ] && vim /tmp/${FILE}
files=$(ls ${FILE} 2> /dev/null | wc -l); 
 
echo $files
if [ "$files" != "0" ] ;then  #如果存在文件
  python run/upload2dpast.py
  # cont=$(cat ${FILE})
  # echo ${cont}
  # Set expiry (1–365 days)
  # curl -s -F "expiry_days=10" -F "${cont}" https://dpaste.com/api/v2/
  # echo "$FILE exists."
  if type nvim > /dev/null 2>&1; then
    alias vim='nvim'
    vim ${FILE}
  else
    type vim
    vim ${FILE}
  fi
fi 

