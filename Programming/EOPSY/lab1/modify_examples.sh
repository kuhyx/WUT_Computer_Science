#!/bin/bash

touch a
touch B
touch SED
mkdir foldera
mkdir FOLDERB
mkdir FOLDERSED
mkdir upperfoldermain
cd upperfoldermain
touch upperfilesub
mkdir upperfoldersub
cd upperfoldersub
touch upperfilesubsub
cd ..
cd ..


mkdir LOWERCASEFOLDERMAIN 
cd LOWERCASEFOLDERMAIN
touch LOWERFILESUB
mkdir LOWERFOLDERSUB
cd LOWERFOLDERSUB
touch LOWERFILESUBSUB
cd ..
cd ..

mkdir SEDLOWERCASEFOLDERMAIN
cd SEDLOWERCASEFOLDERMAIN
touch SEDLOWERFILESUB
mkdir SEDLOWERFOLDERSUB
cd SEDLOWERFOLDERSUB
touch SEDLOWERFILESUBSUB
cd ..
cd ..

touch recursefile
touch RECURSELOWERFILE
touch SEDRECURSEFILE



echo "Typical scenarios"
echo "Uppercasing file with filename a"
bash ./modify.sh -u a
echo "Lowercasing file with filename B"
bash ./modify.sh -l B
echo "Using sed pattern for lowercasing of file with filename SED"
bash ./modify.sh "-r -e s/.*/\L&/" SED 
echo "Uppercasing folder with name foldera non recursively"
bash ./modify.sh -u foldera
echo "Lowercasing folder with name FOLDERB non recursively"
bash ./modify.sh -l FOLDERB
echo "Using sed pattern for lowercasing of folder with name FOLDERSED non recursively"
bash ./modify.sh "-l -e s/.*/\L&/" FOLDERSED
echo "Uppercasing folder recursively"
echo "Main folder name: upperfoldermain"
echo "folder contains: folder named upperfoldersub , file named upperfilesub"
echo "subfolder upperfoldersub contains file named upperfilesubsub"
bash ./modify.sh -r -u upperfoldermain
echo "Lowercasing folder recursively"
echo "Main folder name: LOWERFOLDERMAIN"
echo "folder contains: folder named LOWERFOLDERSUB , file named LOWERFILESUB"
echo "subfolder LOWERFOLDERSUB contains file named LOWERFILESUBSUB"
bash ./modify.sh -r -l SEDLOWERCASEFOLDERMAIN
echo "using sed pattern for Lowercasing folder recursively"
echo "Main folder name: SEDLOWERFOLDERMAIN"
echo "folder contains: folder named SEDLOWERFOLDERSUB , file named SEDLOWERFILESUB"
echo "subfolder SEDLOWERFOLDERSUB contains file named SEDLOWERFILESUBSUB"
bash ./modify.sh -r "-r -e s/.*/\L&/" SEDLOWERFOLDERMAIN
echo "Uncommon scenarios"
echo "uppercasing recursively normal file recursefile"
bash ./modify.sh -r -u recursefile
echo "lowercasing recursively normal file RECURSELOWERFILE"
bash ./modify.sh -r -l RECURSELOWERFILE
echo "using sed pattern recursively for normal file to lowercase it SEDRECURSEFILE"
bash ./modify.sh -r "-r -e s/.*/\L&/" SEDRECURSEFILE
echo "Incorrect scenarios"
echo "not providing enough arguments"
bash ./modify.sh
echo "not providing file"
bash ./modify.sh -l
echo "not providing argument for recursion"
bash ./modify.sh -r filename
echo "provding filename/foldername for file/folder which does not exist"
bash ./modify.sh -l thisfiledoesnotexist


