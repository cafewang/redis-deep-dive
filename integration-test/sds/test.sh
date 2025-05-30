#! /bin/bash

oneTimeSetUp() {
  pythondir=`gdb -q --command=../pythondir.gdb`
  redisdir="../../redis-8.0.0"
  cp ../gdb_util.py $pythondir
}

testSds5Struct() {
  export testFunction=${FUNCNAME[0]}
  gdb -q -ex='source test.py' --args $redisdir"/src/redis-server" $redisdir"/redis.conf"
}

testSds8Struct() {
  export testFunction=${FUNCNAME[0]}
  gdb -q -ex='source test.py' --args $redisdir"/src/redis-server" $redisdir"/redis.conf"
}

testSdsGrowZero() {
  export testFunction=${FUNCNAME[0]}
  gdb -q -ex='source test.py' --args $redisdir"/src/redis-server" $redisdir"/redis.conf"
}

testSdscatfmt() {
  export testFunction=${FUNCNAME[0]}
  gdb -q -ex='source test.py' --args $redisdir"/src/redis-server" $redisdir"/redis.conf"
}

. ../../shunit2-2.1.8/shunit2