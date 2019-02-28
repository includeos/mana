pipeline {
  agent { label 'ubuntu-18.04' }

  environment {
    PROFILE_x86_64 = 'clang-6.0-linux-x86_64'
    PROFILE_x86 = 'clang-6.0-linux-x86'
    CPUS = """${sh(returnStdout: true, script: 'nproc')}"""
    CC = 'clang-6.0'
    CXX = 'clang++-6.0'
  }

  stages {
    stage('Setup') {
      steps {
        sh 'mkdir -p install'
        sh 'cp conan/profiles/* ~/.conan/profiles/'
      }
    }
    stage('Unit tests') {
      steps {
        sh script: "mkdir -p unittests", label: "Setup"
        sh script: "cd unittests; env CC=gcc CXX=g++ cmake ../test/unit", label: "Cmake"
        sh script: "cd unittests; make -j $CPUS", label: "Make"
        sh script: "cd unittests; ctest", label: "Ctest"
      }
    }
    stage('Build mana') {
      steps {
        sh script: "mkdir -p build", label: "Setup"
        sh script: "cd build; conan install .. -pr $PROFILE_x86_64", label: "conan install"
        sh script: "cd build; cmake .. 
	sh script: "cd build; make -j $CPUS", label: "Make"
      }
    }
  }
}
