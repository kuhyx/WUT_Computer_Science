-- CreateTable
CREATE TABLE "example_table" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100),
    "created_at" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "example_table_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "HelloWorld" (
    "id" SERIAL NOT NULL,
    "message" TEXT NOT NULL,

    CONSTRAINT "HelloWorld_pkey" PRIMARY KEY ("id")
);
