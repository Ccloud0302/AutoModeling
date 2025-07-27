https://blog.csdn.net/L_ZG_/article/details/105363109

元素限定

![image-20241204172704912](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204172704912.png)

属性限定

![image-20241204172748545](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204172748545.png)





在 XML Schema Definition (XSD) 中，约束条件用于定义 XML 文档的结构和数据类型。XSD 通过一系列的约束条件来确保 XML 数据的正确性和一致性。以下是 XSD 中常见的约束条件：





### 1. **基本数据类型约束**

- **`xs:string`**: 定义一个字符串类型。
- **`xs:int`**, **`xs:integer`**: 定义整数类型。
- **`xs:float`**, **`xs:double`**: 定义浮动类型的数值。
- **`xs:boolean`**: 定义布尔类型（`true` 或 `false`）。
- **`xs:date`**, **`xs:dateTime`**: 定义日期和日期时间类型。

### 2. **元素和属性约束**

- **`minOccurs` 和 `maxOccurs`**: 这是指示器约束！

  - 用来限制元素的出现次数。`minOccurs` 是最小出现次数，`maxOccurs` 是最大出现次数。

  - 例如：

    ```
    xml
    
    
    复制代码
    <xs:element name="item" minOccurs="1" maxOccurs="unbounded"/>
    ```

  - `unbounded` 表示没有上限。

  - **属性：minOccurs 和 maxOccurs**

    - 设元素 `el` 的出现次数为 `x`，则：

    ![image-20241204170135923](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170135923.png)

    其中，`x` 是元素 `el` 在 XML 中的实际出现次数，`minOccurs` 和 `maxOccurs` 分别是该元素的最小和最大出现次数。

- **`default` 和 `fixed`**:

  - `default` 用于为元素或属性提供默认值。

  - `fixed` 用于强制元素或属性的值固定不变。

  - 例如：

    ```
    xml
    
    
    复制代码
    <xs:element name="color" type="xs:string" default="red"/>
    ```

    `default` 属性指定元素的默认值。如果在 XML 实例中没有提供该元素的值，则使用 `default` 值。

    设元素 `el` 的默认值为 `d`，如果 XML 文档中没有提供 `el` 的值，则： 

    ![image-20241204170502614](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170502614.png)

    其中，`v(el)` 是元素 `el` 的值，`d` 是 `el` 的默认值。



​			`fixed` 属性指定元素的固定值。在 XML 中，元素的值必须等于固定值 `f`。

​			设元素 `el` 的固定值为 `f`，则：

​			![image-20241204170531194](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170531194.png)

​			其中，`v(el)` 是元素 `el` 的值，`f` 是该元素的固定值。

- **`required`**:

  - `required` 属性用于确保元素必须出现。

  - 例如：

    ```
    xml
    
    
    复制代码
    <xs:element name="name" type="xs:string" minOccurs="1"/>
    ```

- ### **属性：unique**

  `unique` 约束确保一个元素的值在父元素中是唯一的。

  设元素 `el` 的值集合为 `V(el)`，在其父元素中，要求： 

  ![image-20241204170609523](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170609523.png)

   其中，`V(el)` 是所有 `el` 元素值的集合。

- ### **属性：key**

  `key` 约束规定元素的值必须唯一，并且可以作为父元素中其他元素的标识符。

  设元素 `el` 的值集合为 `V(el)`，且该值可以用作标识符，要求：

  ![image-20241204170739749](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170739749.png)

  并且该值在父元素中可用于唯一标识其他元素。

  ### **属性：keyref**

  `keyref` 是 `key` 约束的扩展，指明某个元素值引用另一个元素的 `key`。

  设元素 `el` 的值为 `v`，它应该与另一个元素 `ref_el` 中的 `key` 约束的值一致： 

  ![image-20241204170829299](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170829299.png)

  其中，`v(el)` 是元素 `el` 的值，`v(ref_el)` 是引用的元素的 `key` 值。

  ### **属性：minInclusive 和 maxInclusive**

  `minInclusive` 和 `maxInclusive` 用于对元素值设置数值范围约束，包含边界。

  设元素 `el` 的值为 `v`，则：

  ![image-20241204170850706](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170850706.png)

   其中，`v` 是元素的值，`minInclusive` 和 `maxInclusive` 是该值允许的最小值和最大值（包括边界值）。

  ### **属性：minExclusive 和 maxExclusive**

  `minExclusive` 和 `maxExclusive` 用于对元素值设置数值范围约束，不包含边界。

  设元素 `el` 的值为 `v`，则： 

  ![image-20241204170936273](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170936273.png)

   其中，`v` 是元素的值，`minExclusive` 和 `maxExclusive` 是该值允许的最小值和最大值（不包括边界值）。

  ### **属性：totalDigits 和 fractionDigits**

  `totalDigits` 约束指定元素值的总数字位数，`fractionDigits` 约束指定小数点后的数字位数。

  设元素 `el` 的值为浮动数 `v`，则：

  ![image-20241204171001959](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204171001959.png)

  其中，`|v|_{\text{total digits}}` 是数字的总位数（包括整数和小数部分），

  `|v|_{\text{fraction digits}}` 是小数部分的位数。

### 3. **模式约束**

| enumeration    | 定义可接受值的一个列表                                    |
| -------------- | --------------------------------------------------------- |
| fractionDigits | 定义所允许的最大的小数位数。必须大于等于0。               |
| length         | 定义所允许的字符或者列表项目的精确数目。必须大于或等于0。 |
| maxExclusive   | 定义数值的上限。所允许的值必须小于此值。                  |
| maxInclusive   | 定义数值的上限。所允许的值必须小于或等于此值。            |
| maxLength      | 定义所允许的字符或者列表项目的最大数目。必须大于或等于0。 |
| minExclusive   | 定义数值的下限。所允许的值必需大于此值。                  |
| minInclusive   | 定义数值的下限。所允许的值必需大于或等于此值。            |
| minLength      | 定义所允许的字符或者列表项目的最小数目。必须大于或等于0。 |
| pattern        | 定义可接受的字符的精确序列。                              |
| totalDigits    | 定义所允许的阿拉伯数字的精确位数。必须大于0。             |
| whiteSpace     | 定义空白字符（换行、回车、空格以及制表符）的处理方式。    |

- **`pattern`**:

  - 使用正则表达式限制元素或属性的值。例如，限定电话号码的格式：

    ```
    xml复制代码<xs:element name="phone" type="xs:string">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:pattern value="\d{3}-\d{4}-\d{4}"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    ```

    **限定：pattern**

    - 设元素 `el` 包含字符串 `s`，如果 `s` 符合正则表达式 `Regex`，则：

    ![image-20241204170214460](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170214460.png)

    其中，`Regex` 是定义的正则表达式，`s` 是该元素的值。

- **`enumeration`**:

  - 限制元素或属性的值只能是列出的某个值。

  - 例如：

    ```
    xml复制代码<xs:element name="gender">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:enumeration value="male"/>
                <xs:enumeration value="female"/>
                <xs:enumeration value="other"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    ```

    **限定：enumeration**

    - 设元素 `el` 的值为 `v`，如果 `v` 属于枚举集合 `E`，则：

    ![image-20241204170233022](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170233022.png)

    其中，`E` 是一个离散的值集合，`v` 是元素的值。

- **`minLength` 和 `maxLength`**:

  - 用于限制字符串的最小长度和最大长度。

  - 例如：

    ```
    xml复制代码<xs:element name="username">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:minLength value="5"/>
                <xs:maxLength value="20"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    ```

    - 设元素 `el` 的值为字符串 `s`，如果字符串 `s` 的长度 `|s|` 满足以下条件：

    ![image-20241204170250459](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170250459.png)

    其中，`|s|` 是字符串 `s` 的长度，`minLength` 和 `maxLength` 是该字符串的最小和最大长度。

- **`length`**:

  - 限制字符串的确切长度。

  - 例如：

    ```
    xml复制代码<xs:element name="code">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:length value="10"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    ```

    - 设元素 `el` 的值为字符串 `s`，如果字符串 `s` 的长度 `|s|` 等于特定值 `L`，则：

    ![image-20241204170306634](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170306634.png)

    其中，`L` 是字符串的固定长度。

### 4. **数据类型的限制和继承**



- **`restriction`**:

  - 用于限制或衍生数据类型。`xs:restriction` 可以基于现有的数据类型进行扩展或限制。

  - 例如：

    ```
    xml复制代码<xs:simpleType name="positiveInteger">
        <xs:restriction base="xs:int">
            <xs:minInclusive value="1"/>
        </xs:restriction>
    </xs:simpleType>
    ```

    设元素 `el` 的值为 `v`，并且该值限制在一个数据类型范围内，如最小值 `minValue` 和最大值 `maxValue`，则：

    ![image-20241204170327147](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170327147.png)

    其中，`v` 是元素的值，`minValue` 和 `maxValue` 分别是该值的最小和最大允许值。

- **`union`**:

  - 允许多个数据类型的联合类型。例如，可以允许整数或浮点数作为值。

  - 例如：

    ```
    xml复制代码<xs:simpleType name="number">
        <xs:union memberTypes="xs:int xs:float"/>
    </xs:simpleType>
    ```

    设定一个 `union` 类型，表示元素 `el` 的值可以是 `T_1, T_2, \dots, T_n` 之一。

    ![image-20241204171224866](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204171224866.png)

    其中，`T_1, T_2, \dots, T_n` 是可以作为 `el` 值的数据类型，`v(el)` 是元素 `el` 的实际值。

- **`list`**:

  - 定义多个值的列表。例如，定义一个整数列表：

    ```
    xml复制代码<xs:simpleType name="integerList">
        <xs:list itemType="xs:int"/>
    </xs:simpleType>
    ```

    设元素 `el` 的值为一个由空格（或其他分隔符）分隔的字符串 `v`，则：

    ![image-20241204171243394](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204171243394.png)

    其中，`v_1, v_2, \dots, v_n` 是分隔符分开的多个值。

### 5. **复杂类型的约束（指示器约束）**

- **`sequence`**:

  - 定义子元素的顺序。

  - 例如：

    ```
    xml复制代码<xs:complexType>
        <xs:sequence>
            <xs:element name="firstName" type="xs:string"/>
            <xs:element name="lastName" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    ```

    设一个复杂类型 `CT` 由多个元素组成，元素 `el1`、`el2`、`el3` 需要按顺序出现，则：

    ![image-20241204170346486](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170346486.png)

    其中，`el1`、`el2` 和 `el3` 必须按给定顺序出现在 XML 中。

- **`choice`**:

  - 允许子元素中的某些元素之一出现在 XML 文档中。

  - 例如：

    ```
    xml复制代码<xs:complexType>
        <xs:choice>
            <xs:element name="phone" type="xs:string"/>
            <xs:element name="email" type="xs:string"/>
        </xs:choice>
    </xs:complexType>
    ```

    设元素 `el` 可以是集合 `S` 中的任一元素（即集合中只能选择一个元素），则：

    ![image-20241204170401503](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170401503.png)

    其中，`S` 是一组可能的元素，`e` 是 `S` 中的一个元素。

- **`all`**:

  - 允许所有子元素出现一次或零次，顺序不重要。

  - 例如：

    ```
    xml复制代码<xs:complexType>
        <xs:all>
            <xs:element name="address" type="xs:string"/>
            <xs:element name="city" type="xs:string"/>
        </xs:all>
    </xs:complexType>
    ```

    设元素 `el1`、`el2` 必须在 XML 中出现一次或零次，顺序不重要，则：

    ![image-20241204170418035](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170418035.png)

    其中，`el1` 和 `el2` 都可以选择性地出现 0 次或 1 次。

### 6. **引用和继承约束**

- **`ref`**:

  - 用于引用其他地方定义的元素或类型。

  - 例如：

    ```
    xml复制代码<xs:element name="address" type="xs:string"/>
    <xs:element ref="address"/>
    ```

    设元素 `el` 引用了定义好的类型 `T`，则：

    ![image-20241204170433657](C:\Users\shiha\AppData\Roaming\Typora\typora-user-images\image-20241204170433657.png)

    其中，`T` 是已定义的复杂类型或元素类型。

- **`type`**:

  - 引用一个类型定义。可以为元素或属性指定已有的复杂类型。

  - 例如：

    ```
    xml
    
    
    复制代码
    <xs:element name="person" type="xs:string"/>
    ```

### 总结：

这些约束条件帮助你在 XML 文件中指定结构、数据类型、值范围和行为规则，从而确保数据的完整性和准确性。在 XSD 中，约束条件的组合使用使得 XML 数据的验证更加灵活和强大。